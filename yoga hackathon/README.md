# MediIntel AI

A complete healthcare AI platform for dynamic medical record intelligence.

## Features
- FastAPI backend with OCR and NLP extraction
- PaddleOCR + OpenCV for image and PDF processing
- SciSpaCy / spaCy entity extraction
- Dynamic dashboard with Plotly charts
- PostgreSQL persistence for documents, patient records, medications, risks, summaries, and chat logs
- Premium Microsoft-style UI with drag-and-drop upload and AI chat assistant
- Docker and Kubernetes manifests for production-ready deployment

## Quick Start

### Option 1: Using Quick Start Script (Easiest)
**Windows:**
```bash
quick-start.bat
```

**macOS/Linux:**
```bash
chmod +x quick-start.sh
./quick-start.sh
```

### Option 2: Manual Docker Setup
```bash
docker compose up --build
```

Then open `http://localhost:8000` in your browser.

## Recent Fixes ✅
- Fixed Pydantic v2 compatibility (orm_mode → from_attributes)
- Fixed OCR result parsing for empty or malformed documents
- Added spaCy model download in Docker build
- Improved .dockerignore for faster builds

## Complete Setup Guide
See **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for:
- Local development setup (without Docker)
- Kubernetes deployment
- Troubleshooting
- API documentation
- Security considerations

## API Endpoints
- `POST /upload` - upload and analyze a medical document
- `POST /analyze` - analyze an existing document by ID
- `GET /patient/{id}` - load a patient dashboard
- `GET /summary/{id}` - get extracted summary
- `GET /risks/{id}` - list risk alerts
- `GET /medications/{id}` - list medications
- `POST /chat` - ask AI questions about the extracted record

## Project Structure
```
mediintel-ai/
├── backend/app/          # FastAPI application
├── frontend/             # HTML/CSS/JS UI
├── k8s/                  # Kubernetes manifests
├── docker-compose.yml    # Docker Compose config
└── requirements.txt      # Python dependencies
```

## Notes
- The dashboard is empty until a real document is uploaded
- Upload medical PDFs, prescriptions, lab reports, or medical images
- Uploaded files are stored in `/app/uploads`
- For production use, change default passwords and use proper secrets management
