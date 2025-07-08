import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple, Any, Optional
import logging
import re
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarityEngine:
    def __init__(self, model_name: str = "tfidf"):
        self.model_name = model_name
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
        
        self.weights = {
            'semantic_similarity': 0.25,
            'skill_match': 0.40,
            'experience_match': 0.15,
            'education_match': 0.05,
            'keyword_match': 0.15
        }
        
        # Predefined skill sets for better matching
        self.skill_categories = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi'],
            'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gitlab'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'r', 'stata', 'spss'],
            'tools': ['git', 'linux', 'bash', 'vim', 'vscode', 'intellij', 'eclipse', 'postman']
        }
        
        logger.info("Initialized lightweight similarity engine with TF-IDF")
    
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
                'detailed_analysis': {},
                'recommendations': [],
                'matched_skills': [],
                'missing_skills': []
            }
    
    def _get_semantic_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate TF-IDF based embeddings as a lightweight alternative to transformers"""
        try:
            if len(texts) == 1:
                # For single text, we need to fit and transform
                embeddings = self.tfidf_vectorizer.fit_transform(texts)
            else:
                # For multiple texts, fit on all and transform all
                embeddings = self.tfidf_vectorizer.fit_transform(texts)
            
            return embeddings.toarray()
        except Exception as e:
            logger.error(f"TF-IDF embedding generation failed: {str(e)}")
            # Return dummy embeddings if TF-IDF fails
            return np.random.rand(len(texts), 100)
    
    def _calculate_semantic_similarity(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_text = self._extract_text_from_data(resume_data)
            job_text = self._extract_text_from_data(job_data)
            
            if not resume_text or not job_text:
                return 0.0
            
            embeddings = self._get_semantic_embeddings([resume_text, job_text])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            return max(0.0, min(1.0, similarity))
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {str(e)}")
            return 0.0
    
    def _calculate_skill_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resume_skills = self._extract_skills(resume_data)
            job_skills = self._extract_skills(job_data)
            
            if not job_skills:
                return {'score': 0.0, 'matched': [], 'missing': []}
            
            matched_skills = []
            for skill in job_skills:
                if any(skill.lower() in resume_skill.lower() or resume_skill.lower() in skill.lower() 
                      for resume_skill in resume_skills):
                    matched_skills.append(skill)
            
            missing_skills = [skill for skill in job_skills if skill not in matched_skills]
            
            score = len(matched_skills) / len(job_skills) if job_skills else 0.0
            
            return {
                'score': score,
                'matched': matched_skills,
                'missing': missing_skills
            }
        except Exception as e:
            logger.error(f"Skill match calculation failed: {str(e)}")
            return {'score': 0.0, 'matched': [], 'missing': []}
    
    def _calculate_experience_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_experience = self._extract_experience_years(resume_data)
            job_experience = self._extract_experience_years(job_data)
            
            if job_experience == 0:
                return 1.0
            
            if resume_experience >= job_experience:
                return 1.0
            else:
                return resume_experience / job_experience
        except Exception as e:
            logger.error(f"Experience match calculation failed: {str(e)}")
            return 0.0
    
    def _calculate_education_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_education = self._extract_education_level(resume_data)
            job_education = self._extract_education_level(job_data)
            
            education_hierarchy = {
                'phd': 6, 'doctorate': 6, 'doctoral': 6,
                'masters': 5, 'master': 5, 'mba': 5, 'ms': 5, 'ma': 5,
                'bachelors': 4, 'bachelor': 4, 'bs': 4, 'ba': 4, 'be': 4,
                'associates': 3, 'associate': 3, 'diploma': 3,
                'high school': 2, 'secondary': 2,
                'none': 1
            }
            
            resume_level = education_hierarchy.get(resume_education.lower(), 1)
            job_level = education_hierarchy.get(job_education.lower(), 1)
            
            if resume_level >= job_level:
                return 1.0
            else:
                return resume_level / job_level
        except Exception as e:
            logger.error(f"Education match calculation failed: {str(e)}")
            return 0.0
    
    def _calculate_keyword_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        try:
            resume_text = self._extract_text_from_data(resume_data).lower()
            job_text = self._extract_text_from_data(job_data).lower()
            
            if not job_text:
                return 0.0
            
            # Extract important keywords from job description
            important_keywords = re.findall(r'\b[a-zA-Z]{3,}\b', job_text)
            important_keywords = [word for word in important_keywords if len(word) > 3]
            
            if not important_keywords:
                return 0.0
            
            matched_keywords = sum(1 for keyword in important_keywords if keyword in resume_text)
            
            return matched_keywords / len(important_keywords)
        except Exception as e:
            logger.error(f"Keyword match calculation failed: {str(e)}")
            return 0.0
    
    def _extract_text_from_data(self, data: Dict[str, Any]) -> str:
        try:
            if 'text' in data:
                return str(data['text'])
            elif 'cleaned_text' in data:
                return str(data['cleaned_text'])
            elif 'raw_text' in data:
                return str(data['raw_text'])
            else:
                # Combine all text fields
                text_parts = []
                for key, value in data.items():
                    if isinstance(value, str) and len(value) > 10:
                        text_parts.append(value)
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, str) and len(subvalue) > 10:
                                text_parts.append(subvalue)
                return ' '.join(text_parts)
        except Exception:
            return ""
    
    def _extract_skills(self, data: Dict[str, Any]) -> List[str]:
        try:
            skills = []
            text = self._extract_text_from_data(data).lower()
            
            # Extract from predefined skill categories
            for category, skill_list in self.skill_categories.items():
                for skill in skill_list:
                    if skill.lower() in text:
                        skills.append(skill)
            
            # Extract from structured data if available
            if 'keywords' in data and isinstance(data['keywords'], dict):
                if 'technical_skills' in data['keywords']:
                    skills.extend([skill['term'] for skill in data['keywords']['technical_skills']])
            
            return list(set(skills))
        except Exception:
            return []
    
    def _extract_experience_years(self, data: Dict[str, Any]) -> int:
        try:
            text = self._extract_text_from_data(data)
            
            # Look for patterns like "5 years", "3+ years", etc.
            experience_patterns = [
                r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
                r'(\d+)\+?\s*years?\s*in',
                r'experience\s*:\s*(\d+)\+?\s*years?',
                r'(\d+)\+?\s*years?\s*working'
            ]
            
            max_years = 0
            for pattern in experience_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        years = int(match)
                        max_years = max(max_years, years)
                    except ValueError:
                        continue
            
            return max_years
        except Exception:
            return 0
    
    def _extract_education_level(self, data: Dict[str, Any]) -> str:
        try:
            text = self._extract_text_from_data(data).lower()
            
            education_keywords = {
                'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
                'masters': ['masters', 'master', 'mba', 'm.s.', 'm.a.', 'ms ', 'ma '],
                'bachelors': ['bachelors', 'bachelor', 'b.s.', 'b.a.', 'bs ', 'ba ', 'be ', 'b.e.'],
                'associates': ['associates', 'associate', 'diploma'],
                'high school': ['high school', 'secondary', '12th']
            }
            
            for level, keywords in education_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return level
            
            return 'none'
        except Exception:
            return 'none'
    
    def _generate_analysis(self, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'strengths': self._identify_strengths(result),
            'weaknesses': self._identify_weaknesses(result),
            'score_breakdown': result['component_scores']
        }
    
    def _identify_strengths(self, result: Dict[str, Any]) -> List[str]:
        strengths = []
        scores = result['component_scores']
        
        if scores.get('skill_match', 0) > 0.7:
            strengths.append("Strong skill alignment with job requirements")
        if scores.get('experience_match', 0) > 0.8:
            strengths.append("Excellent experience match")
        if scores.get('semantic_similarity', 0) > 0.6:
            strengths.append("Good semantic relevance to job description")
        if scores.get('keyword_match', 0) > 0.5:
            strengths.append("Good keyword coverage")
        
        return strengths
    
    def _identify_weaknesses(self, result: Dict[str, Any]) -> List[str]:
        weaknesses = []
        scores = result['component_scores']
        
        if scores.get('skill_match', 0) < 0.3:
            weaknesses.append("Limited skill match with job requirements")
        if scores.get('experience_match', 0) < 0.5:
            weaknesses.append("Experience level below job requirements")
        if scores.get('semantic_similarity', 0) < 0.3:
            weaknesses.append("Low semantic relevance to job description")
        if len(result.get('missing_skills', [])) > 3:
            weaknesses.append("Several key skills missing")
        
        return weaknesses
    
    def _generate_recommendations(self, result: Dict[str, Any]) -> List[str]:
        recommendations = []
        missing_skills = result.get('missing_skills', [])
        
        if missing_skills:
            recommendations.append(f"Consider gaining experience in: {', '.join(missing_skills[:5])}")
        
        if result['component_scores'].get('experience_match', 0) < 0.7:
            recommendations.append("Highlight relevant experience more prominently")
        
        if result['component_scores'].get('keyword_match', 0) < 0.5:
            recommendations.append("Include more relevant keywords from the job description")
        
        if result['component_scores'].get('semantic_similarity', 0) < 0.5:
            recommendations.append("Tailor resume content to better match the job description")
        
        return recommendations[:5]  # Limit to top 5 recommendations
