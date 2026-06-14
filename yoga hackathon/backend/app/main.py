import os
from pathlib import Path
print("STEP 1")

from .database import SessionLocal, engine, Base

print("STEP 2")

from .schemas import DashboardResponse, ChatRequest, ChatResponse, AnalyzeRequest

print("STEP 3")

from .services.document_service import analyze_uploaded_document, analyze_existing_document

print("STEP 4")

from .services.nlp_service import answer_question

print("STEP 5")
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .schemas import DashboardResponse, ChatRequest, ChatResponse, AnalyzeRequest
#from .services.document_service import analyze_uploaded_document, analyze_existing_document
#from .services.nlp_service import answer_question
from . import crud
from .config import settings

app = FastAPI(title=settings.app_name)
frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    upload_path = Path(settings.upload_folder)
    upload_path.mkdir(parents=True, exist_ok=True)


@app.post("/upload", response_model=DashboardResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    payload = analyze_uploaded_document(
        file_bytes=file_bytes,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        upload_dir=Path(settings.upload_folder),
        db=db,
    )
    return {
        "patient": payload["patient"],
        "medications": payload["medications"],
        "risks": payload["risks"],
        "summary": payload["summary"],
    }


@app.post("/analyze", response_model=DashboardResponse)
def analyze_document(request: AnalyzeRequest, db: Session = Depends(get_db)):
    payload = analyze_existing_document(request.document_id, db)
    if not payload:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {
        "patient": payload["patient"],
        "medications": payload["medications"],
        "risks": payload["risks"],
        "summary": payload["summary"],
    }


@app.get("/patient/{patient_id}", response_model=DashboardResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    record = crud.get_patient_record(db, patient_id)
    if not record:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    return {
        "patient": record,
        "medications": crud.get_medications(db, patient_id),
        "risks": crud.get_risks(db, patient_id),
        "summary": record.summary,
    }


@app.get("/summary/{patient_id}")
def get_summary(patient_id: int, db: Session = Depends(get_db)):
    record = crud.get_patient_record(db, patient_id)
    if not record:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    return {"summary": record.summary or "No summary available."}


@app.get("/risks/{patient_id}")
def get_risks(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_risks(db, patient_id)


@app.get("/medications/{patient_id}")
def get_medications(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_medications(db, patient_id)


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    record = crud.get_patient_record(db, request.patient_id)
    if not record:
        raise HTTPException(status_code=404, detail="Patient record not found.")
    extracted = record.extracted_json or {}
    answer = answer_question(extracted, request.question)
    crud.create_chat_message(db, patient_id=request.patient_id, question=request.question, answer=answer)
    return {"answer": answer}


@app.get("/")
def serve_index():
    index = frontend_dir / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"status": "MediIntel AI backend is running."}


@app.get("/health")
def health():
    print("HEALTH ROUTE HIT")
    return {"status": "ok"}