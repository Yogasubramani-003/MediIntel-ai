from pathlib import Path
from sqlalchemy.orm import Session
from .ocr_service_simple import extract_text_from_path, save_upload_file
from .nlp_service import generate_summary, parse_medical_entities
from .risk_engine import compute_risks
from .. import crud


def analyze_uploaded_document(file_bytes: bytes, filename: str, content_type: str, upload_dir: Path, db: Session):
    saved_path = save_upload_file(file_bytes, filename, upload_dir)
    document = crud.create_document(db, filename=filename, content_type=content_type, path=saved_path)
    raw_text = extract_text_from_path(saved_path, content_type)
    extracted = parse_medical_entities(raw_text)
    summary = generate_summary(extracted)
    record = crud.create_patient_record(db, extracted, summary, document.id)
    medications = [crud.create_medication(db, record.id, med) for med in extracted.get("medications", [])]
    risks = [crud.create_risk_alert(db, record.id, risk) for risk in compute_risks(extracted)]
    return {
        "patient": record,
        "medications": medications,
        "risks": risks,
        "summary": summary,
    }


def analyze_existing_document(document_id: int, db: Session):
    document = crud.get_document(db, document_id)
    if not document:
        return None
    raw_text = extract_text_from_path(document.path, document.content_type)
    extracted = parse_medical_entities(raw_text)
    summary = generate_summary(extracted)
    record = crud.create_patient_record(db, extracted, summary, document.id)
    medications = [crud.create_medication(db, record.id, med) for med in extracted.get("medications", [])]
    risks = [crud.create_risk_alert(db, record.id, risk) for risk in compute_risks(extracted)]
    return {
        "patient": record,
        "medications": medications,
        "risks": risks,
        "summary": summary,
    }
