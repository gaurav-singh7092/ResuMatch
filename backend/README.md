# ResuMatch Backend

This directory contains the backend Python application for ResuMatch - an AI-powered resume analysis tool.

## Structure

```
backend/
├── main.py                 # Main Flask application
├── config.py              # Configuration settings
├── similarity_engine.py   # Core matching algorithm
├── text_extractor.py      # Text extraction from documents
├── text_preprocessor.py   # Text preprocessing utilities
├── examples.py            # Example scripts and demos
├── requirements.txt       # Python dependencies
├── examples/              # Sample files and results
├── results/               # Analysis output files
├── static/                # Static web assets
├── templates/             # HTML templates
└── uploads/               # Uploaded files storage
```

## Core Components

### `main.py`
The main Flask application that provides the web API for resume analysis.

### `similarity_engine.py`
Contains the core algorithms for:
- Resume-job description matching
- Skill extraction and comparison
- Scoring calculations

### `text_extractor.py`
Handles text extraction from various file formats:
- PDF documents
- Word documents (DOC/DOCX)
- Plain text files
- Image files (OCR)

### `text_preprocessor.py`
Text preprocessing utilities including:
- Text cleaning and normalization
- Tokenization
- Stop word removal
- Feature extraction

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application
```bash
python main.py
```

### Examples
```bash
python examples.py
```

## API Endpoints

The backend provides RESTful API endpoints for the frontend:

- `POST /api/analyze` - Analyze resume against job description
- `GET /api/health` - Health check endpoint
- `GET /api/supported-types` - Get supported file types

## Development

- All Python files follow PEP 8 style guidelines
- Use type hints where applicable
- Include docstrings for all functions and classes
- Add unit tests in the `tests/` directory (to be created)

## Dependencies

See `requirements.txt` for the complete list of Python dependencies.
