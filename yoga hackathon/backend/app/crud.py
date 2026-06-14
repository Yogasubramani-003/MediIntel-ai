from sqlalchemy.orm import Session
from . import models


def create_document(db: Session, filename: str, content_type: str, path: str):
    document = models.Document(filename=filename, content_type=content_type, path=path)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def create_patient_record(db: Session, extracted: dict, summary: str, document_id: int):
    record = models.PatientRecord(
        document_id=document_id,
        name=extracted.get("patient_name"),
        patient_id=extracted.get("patient_id"),
        age=extracted.get("age"),
        gender=extracted.get("gender"),
        dob=extracted.get("dob"),
        blood_group=extracted.get("blood_group"),
        disease=extracted.get("disease"),
        diagnosis=extracted.get("diagnosis"),
        symptoms=extracted.get("symptoms"),
        allergies=extracted.get("allergies"),
        medical_history=extracted.get("medical_history"),
        blood_pressure=extracted.get("blood_pressure"),
        heart_rate=extracted.get("heart_rate"),
        temperature=extracted.get("temperature"),
        oxygen_saturation=extracted.get("oxygen_saturation"),
        hemoglobin=extracted.get("hemoglobin"),
        wbc=extracted.get("wbc"),
        rbc=extracted.get("rbc"),
        platelets=extracted.get("platelets"),
        glucose=extracted.get("glucose"),
        cholesterol=extracted.get("cholesterol"),
        summary=summary,
        extracted_json=extracted,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_medication(db: Session, patient_id: int, medication: dict):
    item = models.Medication(
        patient_id=patient_id,
        drug_name=medication.get("drug_name"),
        dosage=medication.get("dosage"),
        frequency=medication.get("frequency"),
        duration=medication.get("duration"),
        raw_text=medication.get("raw_text"),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_risk_alert(db: Session, patient_id: int, alert: dict):
    item = models.RiskAlert(
        patient_id=patient_id,
        title=alert.get("title"),
        description=alert.get("description"),
        severity=alert.get("severity"),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_chat_message(db: Session, patient_id: int, question: str, answer: str):
    message = models.ChatMessage(
        patient_id=patient_id,
        question=question,
        answer=answer,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_patient_record(db: Session, patient_id: int):
    return db.query(models.PatientRecord).filter(models.PatientRecord.id == patient_id).first()


def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_medications(db: Session, patient_id: int):
    return db.query(models.Medication).filter(models.Medication.patient_id == patient_id).all()


def get_risks(db: Session, patient_id: int):
    return db.query(models.RiskAlert).filter(models.RiskAlert.patient_id == patient_id).all()


def get_chat_history(db: Session, patient_id: int):
    return db.query(models.ChatMessage).filter(models.ChatMessage.patient_id == patient_id).order_by(models.ChatMessage.created_at.asc()).all()
