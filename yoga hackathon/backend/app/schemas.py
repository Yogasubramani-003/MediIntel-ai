from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MedicationSchema(BaseModel):
    drug_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    raw_text: Optional[str] = None

    class Config:
        from_attributes = True


class RiskAlertSchema(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str

    class Config:
        from_attributes = True


class PatientRecordSchema(BaseModel):
    id: int
    name: Optional[str] = None
    patient_id: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    blood_group: Optional[str] = None
    disease: Optional[str] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[str] = None
    temperature: Optional[str] = None
    oxygen_saturation: Optional[str] = None
    hemoglobin: Optional[str] = None
    wbc: Optional[str] = None
    rbc: Optional[str] = None
    platelets: Optional[str] = None
    glucose: Optional[str] = None
    cholesterol: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    patient: PatientRecordSchema
    medications: List[MedicationSchema]
    risks: List[RiskAlertSchema]
    summary: Optional[str] = None


class ChatRequest(BaseModel):
    patient_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str


class AnalyzeRequest(BaseModel):
    document_id: int
