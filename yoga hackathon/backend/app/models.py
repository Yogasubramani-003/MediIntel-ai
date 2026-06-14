from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(256), nullable=False)
    content_type = Column(String(128), nullable=False)
    path = Column(String(1024), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    record = relationship("PatientRecord", back_populates="document", uselist=False)


class PatientRecord(Base):
    __tablename__ = "patient_records"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    name = Column(String(256), nullable=True)
    patient_id = Column(String(128), nullable=True)
    age = Column(String(64), nullable=True)
    gender = Column(String(64), nullable=True)
    dob = Column(String(64), nullable=True)
    blood_group = Column(String(32), nullable=True)
    disease = Column(String(256), nullable=True)
    diagnosis = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    blood_pressure = Column(String(64), nullable=True)
    heart_rate = Column(String(64), nullable=True)
    temperature = Column(String(64), nullable=True)
    oxygen_saturation = Column(String(64), nullable=True)
    hemoglobin = Column(String(64), nullable=True)
    wbc = Column(String(64), nullable=True)
    rbc = Column(String(64), nullable=True)
    platelets = Column(String(64), nullable=True)
    glucose = Column(String(64), nullable=True)
    cholesterol = Column(String(64), nullable=True)
    summary = Column(Text, nullable=True)
    extracted_json = Column(JSON, nullable=True)  # Changed from JSONB to JSON for SQLite
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="record")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    risks = relationship("RiskAlert", back_populates="patient", cascade="all, delete-orphan")
    chats = relationship("ChatMessage", back_populates="patient", cascade="all, delete-orphan")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_records.id"), nullable=False)
    drug_name = Column(String(256), nullable=False)
    dosage = Column(String(128), nullable=True)
    frequency = Column(String(128), nullable=True)
    duration = Column(String(128), nullable=True)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("PatientRecord", back_populates="medications")


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_records.id"), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("PatientRecord", back_populates="risks")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_records.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("PatientRecord", back_populates="chats")
