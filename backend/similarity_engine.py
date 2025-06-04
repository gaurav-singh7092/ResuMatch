import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List, Tuple, Any, Optional
import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.sentence_model = None
        self.tokenizer = None
        self.model = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        
        self.weights = {
            'semantic_similarity': 0.25,
            'skill_match': 0.40,
            'experience_match': 0.15,
            'education_match': 0.05,
            'keyword_match': 0.15
        }
        
        # Load models during initialization
        self._load_models()
    
    def _load_models(self):
        try:
            self.sentence_model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded SentenceTransformer: {self.model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.model = AutoModel.from_pretrained('bert-base-uncased')
            logger.info("Loaded BERT model as backup")
            
        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            try:
                self.sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
                logger.info("Loaded fallback SentenceTransformer model")
            except:
                logger.warning("No transformer models available, using TF-IDF only")
    
    def calculate_similarity(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = {
                'overall_score': 0.0,
                'component_scores': {},
                'detailed_analysis': {},
                'recommendations': [],
                'matched_skills': [],
                'missing_skills': []
            }
            
            semantic_score = self._calculate_semantic_similarity(resume_data, job_data)
            result['component_scores']['semantic_similarity'] = semantic_score
            
            skill_analysis = self._calculate_skill_match(resume_data, job_data)
            result['component_scores']['skill_match'] = skill_analysis['score']
            result['matched_skills'] = skill_analysis['matched']
            result['missing_skills'] = skill_analysis['missing']
            
            experience_score = self._calculate_experience_match(resume_data, job_data)
            result['component_scores']['experience_match'] = experience_score
            
            education_score = self._calculate_education_match(resume_data, job_data)
            result['component_scores']['education_match'] = education_score
            
            keyword_score = self._calculate_keyword_match(resume_data, job_data)
            result['component_scores']['keyword_match'] = keyword_score
            
            overall_score = 0
            for component, score in result['component_scores'].items():
                weight = self.weights.get(component, 0)
                overall_score += score * weight
                
            boosted_score = overall_score ** 0.75

            final_score = min(100.0, boosted_score * 100 * 1.15)
            
            result['overall_score'] = round(final_score, 2)
            
            result['detailed_analysis'] = self._generate_analysis(result)
            
            result['recommendations'] = self._generate_recommendations(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {str(e)}")
            return {
                'overall_score': 0.0,
                'component_scores': {},
                'detailed_analysis': {'error': str(e)},
                'recommendations': [],
                'matched_skills': [],
                'missing_skills': []
            }
    
    def _calculate_semantic_similarity(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_text = resume_data.get('text_features', {}).get('processed_text', '')
            job_text = job_data.get('text_features', {}).get('processed_text', '')
            
            if not resume_text or not job_text:
                return 0.0
            
            if self.sentence_model:
                try:
                    resume_embedding = self.sentence_model.encode(resume_text)
                    job_embedding = self.sentence_model.encode(job_text)
                    
                    similarity = cosine_similarity([resume_embedding], [job_embedding])[0][0]
                    return float(similarity)
                    
                except Exception as e:
                    logger.warning(f"SentenceTransformer failed: {str(e)}")
            
            if self.tokenizer and self.model:
                try:
                    resume_embedding = self._get_bert_embedding(resume_text)
                    job_embedding = self._get_bert_embedding(job_text)
                    
                    similarity = cosine_similarity([resume_embedding], [job_embedding])[0][0]
                    return float(similarity)
                    
                except Exception as e:
                    logger.warning(f"BERT embedding failed: {str(e)}")
            
            try:
                tfidf_matrix = self.tfidf_vectorizer.fit_transform([resume_text, job_text])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(similarity)
                
            except Exception as e:
                logger.warning(f"TF-IDF fallback failed: {str(e)}")
                return 0.0
                
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {str(e)}")
            return 0.0
    
    def _get_bert_embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, 
                               padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
            
        return embeddings.numpy().flatten()
    
    def _calculate_skill_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resume_skills = resume_data.get('skill_features', {})
            job_skills = job_data.get('skill_features', {})
            
            resume_all_skills = set()
            job_all_skills = set()
            
            for category in ['programming_languages', 'frameworks_libraries', 'databases', 'tools_platforms']:
                resume_category_skills = resume_skills.get(f'{category}_list', [])
                job_category_skills = job_skills.get(f'{category}_list', [])
                
                resume_all_skills.update(resume_category_skills)
                job_all_skills.update(job_category_skills)
            
            if not job_all_skills:
                return {'score': 0.0, 'matched': [], 'missing': []}
            
            matched_skills = list(resume_all_skills.intersection(job_all_skills))
            missing_skills = list(job_all_skills - resume_all_skills)
            
            if len(job_all_skills) > 0:
                score = len(matched_skills) / len(job_all_skills)
            else:
                score = 0.0
            
            return {
                'score': score,
                'matched': matched_skills,
                'missing': missing_skills
            }
            
        except Exception as e:
            logger.error(f"Skill matching failed: {str(e)}")
            return {'score': 0.0, 'matched': [], 'missing': []}
    
    def _calculate_experience_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_skills = resume_data.get('skill_features', {})
            job_skills = job_data.get('skill_features', {})
            
            resume_years = resume_skills.get('years_experience', [])
            job_years = job_skills.get('years_experience', [])
            
            if not resume_years or not job_years:
                return 0.5
            
            max_resume_years = max(resume_years)
            min_job_years = min(job_years)
            
            if max_resume_years >= min_job_years:
                over_ratio = max_resume_years / min_job_years
                return min(1.0, 0.7 + (over_ratio - 1) * 0.3)
            else:
                return max(0.0, max_resume_years / min_job_years * 0.6)
                
        except Exception as e:
            logger.error(f"Experience matching failed: {str(e)}")
            return 0.5
    
    def _calculate_education_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_sections = resume_data.get('section_features', {})
            job_sections = job_data.get('section_features', {})
            
            resume_has_education = resume_sections.get('has_education', False)
            job_requires_education = job_sections.get('has_education', False)
            
            if not job_requires_education:
                return 1.0
            
            if resume_has_education and job_requires_education:
                return 0.8
            elif resume_has_education:
                return 0.6
            else:
                return 0.2
                
        except Exception as e:
            logger.error(f"Education matching failed: {str(e)}")
            return 0.5
    
    def _calculate_keyword_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_text = resume_data.get('text_features', {}).get('processed_text', '')
            job_text = job_data.get('text_features', {}).get('processed_text', '')
            
            if not resume_text or not job_text:
                return 0.0
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Keyword matching failed: {str(e)}")
            return 0.0
    
    def _generate_analysis(self, result: Dict[str, Any]) -> Dict[str, Any]:
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'score_breakdown': {}
        }
        
        try:
            scores = result['component_scores']
            
            for component, score in scores.items():
                percentage = score * 100
                analysis['score_breakdown'][component] = f"{percentage:.1f}%"
                
                if score >= 0.6:
                    analysis['strengths'].append(f"Strong {component.replace('_', ' ')}")
                elif score <= 0.25:
                    analysis['weaknesses'].append(f"Weak {component.replace('_', ' ')}")
            
            overall = result['overall_score']
            if overall >= 75:
                analysis['overall_assessment'] = "Excellent match"
            elif overall >= 60:
                analysis['overall_assessment'] = "Good match"
            elif overall >= 45:
                analysis['overall_assessment'] = "Fair match"
            else:
                analysis['overall_assessment'] = "Poor match"
                
        except Exception as e:
            logger.error(f"Analysis generation failed: {str(e)}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _generate_recommendations(self, result: Dict[str, Any]) -> List[str]:
        recommendations = []
        
        try:
            scores = result['component_scores']
            missing_skills = result.get('missing_skills', [])
            
            if scores.get('skill_match', 0) < 0.5 and missing_skills:
                top_missing = missing_skills[:5]
                recommendations.append(f"Consider adding these skills: {', '.join(top_missing)}")
            
            if scores.get('semantic_similarity', 0) < 0.4:
                recommendations.append("Include more relevant keywords from the job description")
                recommendations.append("Tailor your resume content to better match the role requirements")
            
            if scores.get('experience_match', 0) < 0.5:
                recommendations.append("Highlight relevant work experience more prominently")
                recommendations.append("Include specific examples of achievements in similar roles")
            
            if scores.get('education_match', 0) < 0.5:
                recommendations.append("Ensure educational qualifications are clearly stated")
                recommendations.append("Consider adding relevant certifications or courses")
            
            if scores.get('keyword_match', 0) < 0.4:
                recommendations.append("Use more industry-specific terminology from the job posting")
                recommendations.append("Include relevant buzzwords and technical terms")
                
        except Exception as e:
            logger.error(f"Recommendation generation failed: {str(e)}")
            recommendations.append("Unable to generate specific recommendations")
        
        return recommendations
    
    def update_weights(self, new_weights: Dict[str, float]):
        if sum(new_weights.values()) != 1.0:
            raise ValueError("Weights must sum to 1.0")
        
        self.weights.update(new_weights)
        logger.info(f"Updated weights: {self.weights}")
    
    def get_similarity_matrix(self, texts: List[str]) -> np.ndarray:
        try:
            if self.sentence_model:
                embeddings = self.sentence_model.encode(texts)
                return cosine_similarity(embeddings)
            else:
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
                return cosine_similarity(tfidf_matrix)
                
        except Exception as e:
            logger.error(f"Similarity matrix calculation failed: {str(e)}")
            return np.zeros((len(texts), len(texts)))
