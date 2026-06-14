# MediIntel AI - Setup and Run Guide

## Overview
MediIntel AI is a healthcare AI platform for medical record intelligence with OCR, NLP extraction, and risk analysis.

## Fixed Issues
✅ Pydantic v2 compatibility (orm_mode → from_attributes)
✅ OCR service result handling for empty documents
✅ SpaCy model download in Docker
✅ Improved .dockerignore for smaller builds

---

## Prerequisites

### Required Software
- **Docker** and **Docker Compose** (recommended)
- **Python 3.12** (for local development)
- **PostgreSQL 15** (if running without Docker)
- **poppler-utils** (for PDF processing)

---

## Quick Start with Docker (Recommended)

### 1. Build and Run
```bash
docker compose up --build
```

### 2. Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

### 3. Stop the Application
```bash
docker compose down
```

### 4. Clean Up (Remove Volumes)
```bash
docker compose down -v
```

---

## Local Development Setup (Without Docker)

### 1. Install System Dependencies

**Windows (using Chocolatey or Scoop):**
```bash
# Install poppler for PDF processing
scoop install poppler
# or
choco install poppler
```

**macOS:**
```bash
brew install poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils build-essential
```

### 2. Set Up PostgreSQL
```bash
# Install PostgreSQL 15
# Create database
psql -U postgres
CREATE DATABASE mediintel;
\q
```

### 3. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/mediintel
UPLOAD_FOLDER=./uploads
DEBUG=False
```

### 5. Run the Application
```bash
# Make sure virtual environment is activated
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Access the Application
```
http://localhost:8000
```

---

## Kubernetes Deployment

### 1. Build Docker Image
```bash
docker build -t mediintel-ai:latest .
```

### 2. Load to Kubernetes (if using local cluster like Minikube)
```bash
# For Minikube
minikube image load mediintel-ai:latest

# For kind
kind load docker-image mediintel-ai:latest
```

### 3. Deploy to Kubernetes
```bash
# Apply secrets first
kubectl apply -f k8s/postgres-secret.yaml

# Deploy applications
kubectl apply -f k8s/deployment.yaml

# Create services
kubectl apply -f k8s/service.yaml
```

### 4. Access the Application
```bash
# Port forward to access locally
kubectl port-forward service/mediintel-web 8000:8000
```

Then open: `http://localhost:8000`

### 5. Check Pod Status
```bash
kubectl get pods
kubectl logs <pod-name>
```

### 6. Clean Up
```bash
kubectl delete -f k8s/
```

---

## Project Structure

```
mediintel-ai/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI application
│       ├── config.py            # Configuration settings
│       ├── database.py          # Database connection
│       ├── models.py            # SQLAlchemy models
│       ├── schemas.py           # Pydantic schemas
│       ├── crud.py              # Database operations
│       └── services/
│           ├── document_service.py  # Document processing
│           ├── ocr_service.py       # OCR with PaddleOCR
│           ├── nlp_service.py       # NLP entity extraction
│           └── risk_engine.py       # Risk analysis
├── frontend/
│   ├── index.html              # UI
│   ├── app.js                  # Frontend logic
│   └── styles.css              # Styling
├── k8s/                        # Kubernetes manifests
├── docker-compose.yml          # Docker Compose config
├── Dockerfile                  # Docker build
└── requirements.txt            # Python dependencies
```

---

## API Endpoints

### Upload Document
```bash
POST /upload
Content-Type: multipart/form-data
Body: file (PDF, JPG, PNG)
```

### Get Patient Dashboard
```bash
GET /patient/{patient_id}
```

### Get Summary
```bash
GET /summary/{patient_id}
```

### Get Risks
```bash
GET /risks/{patient_id}
```

### Get Medications
```bash
GET /medications/{patient_id}
```

### Chat with AI
```bash
POST /chat
Content-Type: application/json
Body: {
  "patient_id": 1,
  "question": "What medications is the patient taking?"
}
```

---

## Testing the Application

### 1. Upload a Test Document
You can upload any of these:
- Medical prescription (PDF/Image)
- Lab report (PDF/Image)
- Hospital discharge summary (PDF/Image)
- Any medical document with text

### 2. Example Test Document Content
Create a text file and save as PDF:
```
Patient Name: John Doe
Patient ID: MRN12345
Age: 45
Gender: Male
Blood Group: O+

Diagnosis: Type 2 Diabetes

Medications:
- Metformin 500mg
- Aspirin 75mg

Lab Results:
Glucose: 180
Hemoglobin: 14.2
WBC: 7.5
```

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in environment variables
- Verify database exists: `psql -U postgres -l`

### Docker Build Issues
```bash
# Clean build
docker compose down -v
docker compose build --no-cache
docker compose up
```

### OCR Not Extracting Text
- Ensure image quality is good (minimum 200 DPI)
- PDF should not be password protected
- Text should be machine-readable (not handwritten)

### spaCy Model Not Found
```bash
# Download manually
python -m spacy download en_core_web_sm
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | postgresql+psycopg2://postgres:postgres@localhost:5432/mediintel | PostgreSQL connection string |
| UPLOAD_FOLDER | /app/uploads | Directory for uploaded files |
| DEBUG | False | Enable debug mode |

---

## Performance Tips

1. **Use Docker** - Simplest setup with all dependencies
2. **Increase DPI** - For PDFs, higher DPI (220+) improves OCR accuracy
3. **Clear Uploads** - Periodically clean `/app/uploads` directory
4. **Database Indexing** - Already configured in models
5. **Production Settings** - Use PostgreSQL with persistent volumes

---

## Security Notes

⚠️ **For Development Only**
- Change default PostgreSQL password in production
- Use environment variables for secrets (not hardcoded)
- Enable HTTPS/TLS for production deployments
- Implement proper authentication and authorization
- Validate and sanitize all file uploads
- Use Kubernetes secrets properly (not plaintext)

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs: `docker compose logs` or `kubectl logs`
3. Verify all dependencies are installed
4. Ensure ports 8000 and 5432 are available

---

## License

Review project license before deployment.
