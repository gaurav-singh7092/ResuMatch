from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aiofiles
import os
import shutil
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from text_extractor import TextExtractor
from text_preprocessor import TextPreprocessor
from similarity_engine import SimilarityEngine


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResuMatch",
    description="AI-Powered Resume-Job Matching Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://resumatch.vercel.app", "https://resumatch-app.vercel.app", "https://resmatchfrontend-crc4bg6mn-gaurav-singhs-projects-9a3381d4.vercel.app", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)




text_extractor = TextExtractor()
text_preprocessor = TextPreprocessor()
similarity_engine = SimilarityEngine()


analysis_results = {}


class ResuMatchAnalyzer:

    def __init__(self):
        self.extractor = text_extractor
        self.preprocessor = text_preprocessor
        self.similarity_engine = similarity_engine

    async def analyze_match(self, resume_file: UploadFile, job_description: str) -> Dict[str, Any]:
        try:
            analysis_id = str(uuid.uuid4())

            logger.info("Extracting text from resume...")
            resume_content = await resume_file.read()

            extraction_result = self.extractor.extract_text(
                resume_file.filename,
                resume_content
            )

            if not extraction_result['success']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to extract text from resume: {extraction_result.get('error', 'Unknown error')}"
                )

            resume_text = extraction_result['text']

            logger.info("Preprocessing texts...")
            resume_processed = self.preprocessor.preprocess_text(resume_text)
            job_processed = self.preprocessor.preprocess_text(job_description)

            logger.info("Extracting features...")
            resume_features = self.preprocessor.get_feature_vector(resume_processed)
            job_features = self.preprocessor.get_feature_vector(job_processed)

            logger.info("Calculating similarity...")
            similarity_result = self.similarity_engine.calculate_similarity(
                resume_features,
                job_features
            )

            analysis_result = {
                'analysis_id': analysis_id,
                'timestamp': datetime.now().isoformat(),
                'resume_file': resume_file.filename,
                'extraction_info': {
                    'file_type': extraction_result['file_type'],
                    'extraction_method': extraction_result['extraction_method'],
                    'metadata': extraction_result.get('metadata', {})
                },
                'resume_analysis': {
                    'statistics': resume_processed.get('statistics', {}),
                    'entities': resume_processed.get('entities', {}),
                    'skills': resume_processed.get('skills', {}),
                    'sections': resume_processed.get('sections', {}),
                    'features': resume_features
                },
                'job_analysis': {
                    'statistics': job_processed.get('statistics', {}),
                    'entities': job_processed.get('entities', {}),
                    'skills': job_processed.get('skills', {}),
                    'sections': job_processed.get('sections', {}),
                    'features': job_features
                },
                'similarity_analysis': similarity_result,
                'quality_scores': {
                    'resume_quality': self.preprocessor._calculate_text_quality_score(
                        resume_text, resume_processed
                    ),
                    'job_quality': self.preprocessor._calculate_text_quality_score(
                        job_description, job_processed
                    )
                }
            }

            analysis_results[analysis_id] = analysis_result

            logger.info(f"Analysis completed successfully. ID: {analysis_id}")
            return analysis_result

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


analyzer = ResuMatchAnalyzer()


@app.get("/")
async def home():
    return {"message": "ResuMatch API", "status": "active"}


@app.post("/analyze")
async def analyze_resume_job_match(
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty")
        allowed_types = {'.pdf', '.doc', '.docx', '.txt'}
        file_ext = os.path.splitext(resume.filename)[1].lower()
        if file_ext not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_ext}. Allowed types: {', '.join(allowed_types)}"
            )
        result = await analyzer.analyze_match(resume, job_description)
        return JSONResponse(content={
            'analysis_id': result['analysis_id'],
            'similarity_analysis': result['similarity_analysis'],
            'timestamp': result['timestamp']
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")

# Add an alias route for the British English spelling
@app.post("/analyse")
async def analyse_resume_job_match(
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Redirect to the original function
    return await analyze_resume_job_match(background_tasks, resume, job_description)

# Also add GET routes to handle incorrect method types with helpful error messages
@app.get("/analyze")
async def analyze_get_method():
    raise HTTPException(
        status_code=405,
        detail="Method not allowed. Use POST for resume analysis with multipart/form-data"
    )

@app.get("/analyse")
async def analyse_get_method():
    raise HTTPException(
        status_code=405,
        detail="Method not allowed. Use POST for resume analysis with multipart/form-data"
    )


@app.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return JSONResponse(content=analysis_results[analysis_id])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/batch-analyze")
async def batch_analyze(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    try:
        if len(resumes) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 resumes allowed per batch")
        results = []
        for resume in resumes:
            try:
                result = await analyzer.analyze_match(resume, job_description)
                results.append({
                    'filename': resume.filename,
                    'analysis_id': result['analysis_id'],
                    'overall_score': result['similarity_analysis']['overall_score'],
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'filename': resume.filename,
                    'error': str(e),
                    'status': 'failed'
                })
        successful_results = [r for r in results if r['status'] == 'success']
        failed_results = [r for r in results if r['status'] == 'failed']
        successful_results.sort(key=lambda x: x['overall_score'], reverse=True)
        return JSONResponse(content={
            'total_resumes': len(resumes),
            'successful': len(successful_results),
            'failed': len(failed_results),
            'results': successful_results + failed_results
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch analysis failed")


@app.get("/api/stats")
async def get_statistics():
    return JSONResponse(content={
        'total_analyses': len(analysis_results),
        'models_loaded': {
            'text_extractor': text_extractor is not None,
            'text_preprocessor': text_preprocessor is not None,
            'similarity_engine': similarity_engine.sentence_model is not None
        },
        'supported_formats': text_extractor.supported_formats,
        'uptime': datetime.now().isoformat()
    })


if __name__ == "__main__":
    logger.info("Starting ResuMatch application...")
    logger.info("Checking model availability...")
    if similarity_engine.sentence_model is None:
        logger.warning("SentenceTransformer model not loaded - some features may be limited")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
