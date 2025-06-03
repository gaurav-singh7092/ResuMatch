import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
import string
from typing import List, Dict, Set, Tuple, Any
import logging


try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except:
    pass


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextPreprocessor:
    
    def __init__(self, language='en'):
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            self.stop_words = set()
        
        self.custom_stop_words = {
            'resume', 'cv', 'curriculum', 'vitae', 'experience', 'education',
            'skills', 'objective', 'summary', 'references', 'available',
            'upon', 'request', 'phone', 'email', 'address'
        }
        self.stop_words.update(self.custom_stop_words)
        
        self.skill_patterns = {
            'programming_languages': [
                r'\b(?:python|java|javascript|typescript|c\+\+|c#|c|ruby|php|swift|kotlin|go|rust|scala|r|matlab|perl|dart|objective-c)\b',
                r'\b(?:html5?|css3?|sql|nosql|xml|json|yaml|toml|sass|scss|less)\b'
            ],
            'frameworks_libraries': [
                r'\b(?:react|angular|vue|django|flask|spring|springboot|nodejs|express|laravel|symfony|rails|asp\.net)\b',
                r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy|matplotlib|seaborn|plotly|opencv|keras)\b',
                r'\b(?:bootstrap|tailwind|jquery|d3\.js|three\.js|electron|react-native|flutter|xamarin)\b'
            ],
            'databases': [
                r'\b(?:mysql|postgresql|mongodb|oracle|sqlite|redis|cassandra|elasticsearch|neo4j|couchdb|dynamodb)\b',
                r'\b(?:mariadb|firestore|cosmosdb|aurora|snowflake|bigquery|redshift)\b'
            ],
            'tools_platforms': [
                r'\b(?:git|github|gitlab|bitbucket|docker|kubernetes|aws|azure|gcp|jenkins|terraform|ansible)\b',
                r'\b(?:jira|confluence|slack|trello|asana|notion|figma|sketch|adobe|photoshop|illustrator)\b',
                r'\b(?:linux|unix|windows|macos|ubuntu|centos|debian|fedora|arch)\b'
            ],
            'cloud_devops': [
                r'\b(?:aws|amazon\s+web\s+services|azure|google\s+cloud|gcp|alibaba\s+cloud|ibm\s+cloud)\b',
                r'\b(?:docker|kubernetes|k8s|helm|istio|prometheus|grafana|elk|splunk|datadog|newrelic)\b',
                r'\b(?:ci\/cd|jenkins|gitlab\s+ci|github\s+actions|travis\s+ci|circle\s+ci|bamboo)\b'
            ],
            'soft_skills': [
                r'\b(?:leadership|communication|teamwork|problem[- ]solving|analytical|creative|innovative)\b',
                r'\b(?:adaptable|flexible|detail[- ]oriented|time\s+management|project\s+management|agile|scrum)\b'
            ],
            'certifications': [
                r'\b(?:aws\s+certified|azure\s+certified|google\s+cloud\s+certified|cissp|cism|cisa|pmp|scrum\s+master)\b',
                r'\b(?:comptia|cisco|microsoft\s+certified|oracle\s+certified|salesforce\s+certified)\b'
            ]
        }
        
        self.education_patterns = {
            'degrees': [
                r'\b(?:bachelor|bs|ba|bsc|beng|btech|masters?|ms|ma|msc|meng|mtech|phd|doctorate|md|jd|mba)\b',
                r'\b(?:associate|diploma|certificate|high\s+school|ged)\b'
            ],
            'fields': [
                r'\b(?:computer\s+science|software\s+engineering|information\s+technology|electrical\s+engineering)\b',
                r'\b(?:mechanical\s+engineering|business\s+administration|marketing|finance|accounting|economics)\b',
                r'\b(?:data\s+science|artificial\s+intelligence|machine\s+learning|cybersecurity|mathematics)\b'
            ]
        }
        
        self.job_title_patterns = [
            r'\b(?:software\s+(?:engineer|developer|architect)|full[- ]stack\s+developer|frontend\s+developer|backend\s+developer)\b',
            r'\b(?:data\s+(?:scientist|analyst|engineer)|machine\s+learning\s+engineer|ai\s+engineer|devops\s+engineer)\b',
            r'\b(?:product\s+manager|project\s+manager|scrum\s+master|technical\s+lead|team\s+lead|senior\s+consultant)\b',
            r'\b(?:cto|ceo|cfo|vp|director|manager|analyst|specialist|coordinator|administrator)\b'
        ]
        
        self.compiled_patterns = {}
        for category, patterns in self.skill_patterns.items():
            self.compiled_patterns[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        
        self.compiled_education_patterns = {}
        for category, patterns in self.education_patterns.items():
            self.compiled_education_patterns[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        
        self.compiled_job_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.job_title_patterns]
    
    def preprocess_text(self, text: str, options: Dict[str, bool] = None) -> Dict[str, Any]:
        if options is None:
            options = {
                'clean_text': True,
                'tokenize': True,
                'remove_stopwords': True,
                'lemmatize': True,
                'extract_entities': True,
                'extract_skills': True,
                'extract_sections': True
            }
        
        result = {
            'original_text': text,
            'cleaned_text': '',
            'tokens': [],
            'processed_tokens': [],
            'entities': {},
            'skills': {},
            'sections': {},
            'statistics': {}
        }
        
        try:
            if options.get('clean_text', True):
                result['cleaned_text'] = self._clean_text(text)
            else:
                result['cleaned_text'] = text
            
            if options.get('tokenize', True):
                result['tokens'] = self._tokenize(result['cleaned_text'])
            
            processed_tokens = result['tokens']
            if options.get('remove_stopwords', True):
                processed_tokens = self._remove_stopwords(processed_tokens)
            
            if options.get('lemmatize', True):
                processed_tokens = self._lemmatize(processed_tokens)
            
            result['processed_tokens'] = processed_tokens
            
            if options.get('extract_entities', True):
                result['entities'] = self._extract_entities(result['cleaned_text'])
            
            if options.get('extract_skills', True):
                result['skills'] = self._extract_skills(text)
            
            if options.get('extract_sections', True):
                result['sections'] = self._extract_sections(text)
            
            result['statistics'] = self._calculate_statistics(text, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Text preprocessing failed: {str(e)}")
            result['error'] = str(e)
            return result
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\/\@\#\%\&\*\+\=]', ' ', text)
        text = re.sub(r'\b(\d{1,2})\/(\d{1,2})\/(\d{2,4})\b', r'\1/\2/\3', text)  # Dates
        text = re.sub(r'\b(\d{3})-(\d{3})-(\d{4})\b', r'\1-\2-\3', text)  # Phone numbers
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' EMAIL ', text)  # Email
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' URL ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        try:
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token not in string.punctuation and len(token) > 1]
            
            return tokens
            
        except Exception as e:
            logger.warning(f"NLTK tokenization failed: {str(e)}, using simple split")
            return text.lower().split()
    
    def _remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from tokens"""
        return [token for token in tokens if token not in self.stop_words]
    
    def _lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens"""
        try:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except Exception as e:
            logger.warning(f"Lemmatization failed: {str(e)}")
            return tokens
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using both spaCy and NLTK"""
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'emails': [],
            'phones': [],
            'urls': []
        }
        
        try:
            if self.nlp:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ['PERSON']:
                        entities['persons'].append(ent.text)
                    elif ent.label_ in ['ORG']:
                        entities['organizations'].append(ent.text)
                    elif ent.label_ in ['GPE', 'LOC']:
                        entities['locations'].append(ent.text)
                    elif ent.label_ in ['DATE']:
                        entities['dates'].append(ent.text)
            
            entities['emails'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            entities['phones'] = re.findall(r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b', text)
            entities['urls'] = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            
            for key in entities:
                entities[key] = list(set(entities[key]))
            
        except Exception as e:
            logger.warning(f"Entity extraction failed: {str(e)}")
        
        return entities
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract technical skills and competencies"""
        skills = {}
        
        for category, patterns in self.compiled_patterns.items():
            found_skills = []
            for pattern in patterns:
                matches = pattern.findall(text)
                found_skills.extend(matches)
            
            skills[category] = list(set([skill.lower() for skill in found_skills]))
        
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in'
        ]
        
        experience_matches = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            experience_matches.extend(matches)
        
        if experience_matches:
            skills['years_experience'] = [int(exp) for exp in experience_matches if exp.isdigit()]
        
        return skills
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract common resume sections"""
        sections = {}
        
        section_patterns = {
            'objective': r'(?:objective|career\s+objective|summary|professional\s+summary|profile)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))',
            'experience': r'(?:experience|work\s+experience|employment|professional\s+experience)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))',
            'education': r'(?:education|academic\s+background|qualifications)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))',
            'skills': r'(?:skills|technical\s+skills|core\s+competencies|technologies)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))',
            'certifications': r'(?:certifications?|certificates?|licenses?)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))',
            'projects': r'(?:projects?|portfolio|key\s+projects)(.*?)(?=\n\s*(?:[A-Z\s]{3,}|\Z))'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
        
        return sections
    
    def _calculate_statistics(self, original_text: str, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate various text statistics"""
        stats = {
            'character_count': len(original_text),
            'word_count': len(original_text.split()),
            'sentence_count': len(sent_tokenize(original_text)),
            'token_count': len(processed_data.get('tokens', [])),
            'processed_token_count': len(processed_data.get('processed_tokens', [])),
            'unique_tokens': len(set(processed_data.get('processed_tokens', []))),
            'entities_found': sum(len(entities) for entities in processed_data.get('entities', {}).values()),
            'skills_found': sum(len(skills) for skills in processed_data.get('skills', {}).values() if isinstance(skills, list))
        }
        
        if stats['token_count'] > 0:
            stats['lexical_diversity'] = stats['unique_tokens'] / stats['token_count']
        else:
            stats['lexical_diversity'] = 0
        
        return stats
    
    def get_feature_vector(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        features = {
            'text_features': {
                'processed_text': ' '.join(processed_data.get('processed_tokens', [])),
                'word_count': processed_data.get('statistics', {}).get('word_count', 0),
                'unique_words': processed_data.get('statistics', {}).get('unique_tokens', 0),
                'lexical_diversity': processed_data.get('statistics', {}).get('lexical_diversity', 0)
            },
            'skill_features': {},
            'entity_features': {},
            'section_features': {}
        }
        
        skills = processed_data.get('skills', {})
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                features['skill_features'][f'{category}_count'] = len(skill_list)
                features['skill_features'][f'{category}_list'] = skill_list
        
        entities = processed_data.get('entities', {})
        for entity_type, entity_list in entities.items():
            features['entity_features'][f'{entity_type}_count'] = len(entity_list)
        
        sections = processed_data.get('sections', {})
        for section_name, section_text in sections.items():
            features['section_features'][f'has_{section_name}'] = bool(section_text)
            features['section_features'][f'{section_name}_length'] = len(section_text.split()) if section_text else 0
        
        return features
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Enhanced contact information extraction"""
        contact_info = {
            'emails': [],
            'phones': [],
            'linkedin': [],
            'github': [],
            'websites': [],
            'addresses': []
        }
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        contact_info['emails'] = re.findall(email_pattern, text)
        
        phone_patterns = [
            r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            r'\b(?:\+?91[-.\s]?)?[6-9][0-9]{9}\b'  # Indian numbers
            r'\b(?:\+?44[-.\s]?)?[0-9]{10,11}\b'    # UK numbers
        ]
        
        for pattern in phone_patterns:
            contact_info['phones'].extend(re.findall(pattern, text))
        
        contact_info['linkedin'] = re.findall(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
        contact_info['github'] = re.findall(r'github\.com/[\w\-]+', text, re.IGNORECASE)
        
        website_pattern = r'(?:https?://)?(?:www\.)?[\w\-]+\.[\w\-]+(?:\.[\w\-]+)*(?:/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?'
        potential_websites = re.findall(website_pattern, text, re.IGNORECASE)
        contact_info['websites'] = [w for w in potential_websites if not any(social in w for social in ['linkedin', 'github'])]
        
        for key in contact_info:
            contact_info[key] = list(set(contact_info[key]))
        
        return contact_info
    
    def _extract_education(self, text: str) -> Dict[str, Any]:
        """Extract education information"""
        education = {
            'degrees': [],
            'institutions': [],
            'fields_of_study': [],
            'graduation_years': [],
            'gpa': []
        }
        
        for patterns in self.compiled_education_patterns['degrees']:
            education['degrees'].extend(patterns.findall(text))
        
        for patterns in self.compiled_education_patterns['fields']:
            education['fields_of_study'].extend(patterns.findall(text))
        
        year_pattern = r'\b(19|20)\d{2}\b'
        potential_years = re.findall(year_pattern, text)
        education['graduation_years'] = [int(year) for year in potential_years if 1980 <= int(year) <= 2030]
        
        gpa_patterns = [
            r'gpa[:\s]*([0-4]\.\d+)',
            r'cgpa[:\s]*([0-9]\.\d+)',
            r'grade[:\s]*([0-4]\.\d+)'
        ]
        
        for pattern in gpa_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education['gpa'].extend([float(gpa) for gpa in matches])
        
        institution_keywords = ['university', 'college', 'institute', 'school', 'academy']
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in institution_keywords):
                words = sentence.split()
                for i, word in enumerate(words):
                    if any(keyword in word.lower() for keyword in institution_keywords):
                        start = max(0, i-3)
                        end = min(len(words), i+4)
                        institution = ' '.join(words[start:end])
                        education['institutions'].append(institution.strip())
        
        for key in education:
            if isinstance(education[key], list):
                education[key] = list(set(education[key]))
        
        return education
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract potential job titles from text"""
        job_titles = []
        
        for pattern in self.compiled_job_patterns:
            matches = pattern.findall(text)
            job_titles.extend(matches)
        
        return list(set(job_titles))
    
    def _calculate_text_quality_score(self, text: str, processed_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate quality metrics for the text"""
        scores = {
            'completeness': 0.0,
            'clarity': 0.0,
            'professionalism': 0.0,
            'technical_depth': 0.0,
            'overall': 0.0
        }
        
        stats = processed_data.get('statistics', {})
        entities = processed_data.get('entities', {})
        skills = processed_data.get('skills', {})
        sections = processed_data.get('sections', {})
        
        completeness_factors = [
            len(entities.get('emails', [])) > 0,
            len(entities.get('phones', [])) > 0,
            len(sections.get('experience', '')) > 50,
            len(sections.get('education', '')) > 20,
            len(sections.get('skills', '')) > 20,
            stats.get('word_count', 0) > 100
        ]
        scores['completeness'] = sum(completeness_factors) / len(completeness_factors)
        
        word_count = stats.get('word_count', 1)
        sentence_count = stats.get('sentence_count', 1)
        avg_words_per_sentence = word_count / sentence_count
        
        if 15 <= avg_words_per_sentence <= 20:
            scores['clarity'] = 1.0
        elif 10 <= avg_words_per_sentence < 15 or 20 < avg_words_per_sentence <= 25:
            scores['clarity'] = 0.8
        else:
            scores['clarity'] = 0.6
        
        total_skills = sum(len(skill_list) for skill_list in skills.values() if isinstance(skill_list, list))
        scores['technical_depth'] = min(total_skills / 10, 1.0)
        
        professional_factors = [
            bool(sections.get('objective') or sections.get('summary')),
            bool(sections.get('experience')),
            bool(sections.get('education')),
            bool(sections.get('skills')),
            len(entities.get('emails', [])) <= 2,
            stats.get('word_count', 0) >= 150
        ]
        scores['professionalism'] = sum(professional_factors) / len(professional_factors)
        
        weights = {
            'completeness': 0.3,
            'clarity': 0.2,
            'professionalism': 0.3,
            'technical_depth': 0.2
        }
        
        scores['overall'] = sum(scores[metric] * weight for metric, weight in weights.items())
        
        return scores
    
    def batch_process(self, texts: List[str], options: Dict[str, bool] = None) -> List[Dict[str, Any]]:
        """Process multiple texts in batch"""
        results = []
        
        for i, text in enumerate(texts):
            try:
                logger.info(f"Processing text {i+1}/{len(texts)}")
                result = self.preprocess_text(text, options)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process text {i+1}: {str(e)}")
                results.append({'error': str(e), 'text_index': i})
        
        return results
    
    def export_results(self, processed_data: Dict[str, Any], format_type: str = 'json') -> str:
        """Export processed data in various formats"""
        import json
        
        if format_type.lower() == 'json':
            return json.dumps(processed_data, indent=2, default=str)
        elif format_type.lower() == 'csv':
            flattened = self._flatten_dict(processed_data)
            import csv
            import io
            
            output = io.StringIO()
            if flattened:
                writer = csv.DictWriter(output, fieldnames=flattened.keys())
                writer.writeheader()
                writer.writerow(flattened)
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if v and isinstance(v[0], (str, int, float)):
                    items.append((new_key, ', '.join(map(str, v))))
                else:
                    items.append((new_key, str(len(v))))
            else:
                items.append((new_key, v))
        return dict(items)