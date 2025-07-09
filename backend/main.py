from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
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


cors_origins_str = os.environ.get("CORS_ORIGINS", "http://localhost:3000,https://resumatchfrontend.vercel.app")
cors_origins = cors_origins_str.split(",")
explicit_domains = [
    "http://localhost:3000",
    "https://resumatchfrontend.vercel.app",
    "https://resmatchfrontend.vercel.app",
    "https://resmatchfrontend-crc4bg6mn-gaurav-singhs-projects-9a3381d4.vercel.app",
    "https://resmatchfrontend-6wcnragsb-gaurav-singhs-projects-9a3381d4.vercel.app"
]
all_origins = list(set(cors_origins + explicit_domains))

# Add wildcard support for development and dynamic Vercel URLs
if os.environ.get("ENVIRONMENT") != "production":
    all_origins.append("*")
logger.info(f"CORS origins: {all_origins}")

app = FastAPI(
    title="ResuMatch",
    description="AI-Powered Resume-Job Matching Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,  
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

@app.post("/analyse")
async def analyse_resume_job_match(
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    return await analyze_resume_job_match(background_tasks, resume, job_description)

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

@app.get("/debug")
async def debug_info():
    import sys
    import platform
    import fastapi
    
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }
    
    return JSONResponse(
        content={
            'api_status': 'online',
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
            'fastapi_version': fastapi.__version__,
            'available_endpoints': [
                {'path': route.path, 'methods': list(route.methods)} 
                for route in app.routes
            ],
            'environment': {
                'cors_origins': os.environ.get('CORS_ORIGINS', 'Not set'),
                'port': os.environ.get('PORT', 'Not set'),
            }
        },
        headers=headers
    )

@app.get("/cors-test")
async def cors_test():
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }
    return JSONResponse(
        content={
            'message': 'CORS is working properly!',
            'timestamp': datetime.now().isoformat(),
            'configured_origins': all_origins,
            'status': 'success'
        },
        headers=headers
    )


@app.get("/status", response_class=HTMLResponse)
async def status_page():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ResuMatch API Status</title>
        <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .status {{ color: #28a745; font-weight: bold; }}
            .endpoint {{ background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .cors-origins {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .test-button {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }}
            .test-button:hover {{ background: #0056b3; }}
            .result {{ margin: 15px 0; padding: 15px; border-radius: 5px; background: #f8f9fa; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 ResuMatch API Status</h1>
            <p class="status">✅ API is online and running</p>
            <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
            
            <h2>📋 Available Endpoints</h2>
            <div class="endpoint"><strong>POST</strong> /analyze - Resume analysis</div>
            <div class="endpoint"><strong>GET</strong> /health - Health check</div>
            <div class="endpoint"><strong>GET</strong> /cors-test - CORS test</div>
            <div class="endpoint"><strong>GET</strong> /debug - Debug information</div>
            
            <h2>🌐 CORS Configuration</h2>
            <div class="cors-origins">
                <strong>Allowed Origins:</strong><br>
                {'<br>'.join(all_origins)}
            </div>
            
            <h2>🧪 Test CORS</h2>
            <button class="test-button" onclick="testCORS()">Test CORS from Browser</button>
            <button class="test-button" onclick="testHealth()">Test Health Endpoint</button>
            
            <div id="test-result" class="result" style="display: none;"></div>
            
            <script>
                async function testCORS() {{
                    const resultDiv = document.getElementById('test-result');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = 'Testing CORS...';
                    
                    try {{
                        const response = await fetch('/cors-test');
                        const data = await response.json();
                        resultDiv.innerHTML = '<strong>✅ CORS Test Success:</strong><br>' + JSON.stringify(data, null, 2);
                        resultDiv.style.background = '#d4edda';
                        resultDiv.style.color = '#155724';
                    }} catch (error) {{
                        resultDiv.innerHTML = '<strong>❌ CORS Test Failed:</strong><br>' + error.message;
                        resultDiv.style.background = '#f8d7da';
                        resultDiv.style.color = '#721c24';
                    }}
                }}
                
                async function testHealth() {{
                    const resultDiv = document.getElementById('test-result');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = 'Testing health endpoint...';
                    
                    try {{
                        const response = await fetch('/health');
                        const data = await response.json();
                        resultDiv.innerHTML = '<strong>✅ Health Test Success:</strong><br>' + JSON.stringify(data, null, 2);
                        resultDiv.style.background = '#d4edda';
                        resultDiv.style.color = '#155724';
                    }} catch (error) {{
                        resultDiv.innerHTML = '<strong>❌ Health Test Failed:</strong><br>' + error.message;
                        resultDiv.style.background = '#f8d7da';
                        resultDiv.style.color = '#721c24';
                    }}
                }}
            </script>
        </div>
    </body>
    </html>
    """
    
    # Set custom headers including CSP to allow inline scripts
    headers = {
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    }
    
    return HTMLResponse(content=html_content, headers=headers)


@app.options("/analyze")
async def options_analyze():
    """Handle CORS preflight requests for analyze endpoint"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.options("/analyse")
async def options_analyse():
    """Handle CORS preflight requests for analyse endpoint"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )


if __name__ == "__main__":
    logger.info("Starting ResuMatch application...")
    logger.info("Using lightweight similarity engine with TF-IDF")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
