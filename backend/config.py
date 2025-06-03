import os
from typing import Dict, Any

class Config:
    APP_NAME = "ResuMatch"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-Powered Resume-Job Matching System"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    RELOAD = os.getenv("RELOAD", "True").lower() == "true"
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.png', '.jpg', '.jpeg'}
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    RESULTS_DIR = os.getenv("RESULTS_DIR", "results")
    DEFAULT_SENTENCE_MODEL = os.getenv("SENTENCE_MODEL", "all-MiniLM-L6-v2")
    BACKUP_SENTENCE_MODEL = os.getenv("BACKUP_SENTENCE_MODEL", "paraphrase-MiniLM-L6-v2")
    USE_GPU = os.getenv("USE_GPU", "False").lower() == "true"
    MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 10))
    PROCESSING_TIMEOUT = int(os.getenv("PROCESSING_TIMEOUT", 300))
    SIMILARITY_WEIGHTS = {
        'semantic_similarity': float(os.getenv("WEIGHT_SEMANTIC", 0.35)),
        'skill_match': float(os.getenv("WEIGHT_SKILL", 0.25)),
        'experience_match': float(os.getenv("WEIGHT_EXPERIENCE", 0.15)),
        'education_match': float(os.getenv("WEIGHT_EDUCATION", 0.10)),
        'keyword_match': float(os.getenv("WEIGHT_KEYWORD", 0.15))
    }
    DEFAULT_PREPROCESSING_OPTIONS = {
        'clean_text': True,
        'tokenize': True,
        'remove_stopwords': True,
        'lemmatize': True,
        'extract_entities': True,
        'extract_skills': True,
        'extract_sections': True
    }
    OCR_CONFIG = r'--oem 3 --psm 6'
    OCR_ENABLED = os.getenv("OCR_ENABLED", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = os.getenv("LOG_FILE", "resumatch.log")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "False").lower() == "true"
    API_KEY = os.getenv("API_KEY", None)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resumatch.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        return {
            'sentence_model': cls.DEFAULT_SENTENCE_MODEL,
            'backup_model': cls.BACKUP_SENTENCE_MODEL,
            'use_gpu': cls.USE_GPU,
            'weights': cls.SIMILARITY_WEIGHTS
        }
    @classmethod
    def get_processing_config(cls) -> Dict[str, Any]:
        return {
            'max_file_size': cls.MAX_FILE_SIZE,
            'allowed_extensions': cls.ALLOWED_EXTENSIONS,
            'max_batch_size': cls.MAX_BATCH_SIZE,
            'timeout': cls.PROCESSING_TIMEOUT,
            'ocr_enabled': cls.OCR_ENABLED,
            'ocr_config': cls.OCR_CONFIG,
            'preprocessing_options': cls.DEFAULT_PREPROCESSING_OPTIONS
        }
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        validation_results = {}
        weight_sum = sum(cls.SIMILARITY_WEIGHTS.values())
        validation_results['weights_valid'] = abs(weight_sum - 1.0) < 0.001
        validation_results['upload_dir_exists'] = os.path.exists(cls.UPLOAD_DIR)
        validation_results['results_dir_exists'] = os.path.exists(cls.RESULTS_DIR)
        validation_results['max_file_size_valid'] = cls.MAX_FILE_SIZE > 0
        validation_results['batch_size_valid'] = 1 <= cls.MAX_BATCH_SIZE <= 100
        return validation_results
class DevelopmentConfig(Config):
    DEBUG = True
    RELOAD = True
    LOG_LEVEL = "DEBUG"
class ProductionConfig(Config):
    DEBUG = False
    RELOAD = False
    LOG_LEVEL = "WARNING"
    MAX_FILE_SIZE = 20 * 1024 * 1024
    MAX_BATCH_SIZE = 5
    PROCESSING_TIMEOUT = 180
class TestingConfig(Config):
    DEBUG = True
    UPLOAD_DIR = "test_uploads"
    RESULTS_DIR = "test_results"
    DATABASE_URL = "sqlite:///:memory:"
def get_config(environment: str = None) -> Config:
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development").lower()
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_map.get(environment, DevelopmentConfig)
config = get_config()
