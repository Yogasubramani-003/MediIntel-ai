import re
from typing import Any, Dict, List

import spacy
from spacy.lang.en import English

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = English()


LABEL_PATTERNS = {
    "patient_name": [
        r"Patient Name[:\-\s]*([A-Z][A-Za-z .,\-]{2,80})",
        r"Name[:\-\s]*([A-Z][A-Za-z .,\-]{2,80})",
    ],
    "patient_id": [
        r"Patient ID[:\-\s]*([A-Z0-9\-]+)",
        r"MRN[:\-\s]*([A-Z0-9\-]+)",
    ],
    "age": [r"Age[:\-\s]*([0-9]{1,3})"],
    "gender": [
        r"Gender[:\-\s]*(Male|Female|Other|M|F)",
        r"Sex[:\-\s]*(Male|Female|Other|M|F)",
    ],
    "dob": [
        r"Date of Birth[:\-\s]*([0-9/\-]{6,12})",
        r"DOB[:\-\s]*([0-9/\-]{6,12})",
    ],
    "blood_group": [
        r"Blood Group[:\-\s]*(A\+|A\-|B\+|B\-|AB\+|AB\-|O\+|O\-)"
    ],
}

LAB_PATTERNS = {
    "hemoglobin": [r"Hemoglobin[:\s]*([0-9]+\.?[0-9]*)"],
    "wbc": [r"WBC[:\s]*([0-9]+\.?[0-9]*)"],
    "rbc": [r"RBC[:\s]*([0-9]+\.?[0-9]*)"],
    "platelets": [r"Platelets[:\s]*([0-9]+\.?[0-9]*)"],
    "glucose": [r"Glucose[:\s]*([0-9]+\.?[0-9]*)"],
    "cholesterol": [r"Cholesterol[:\s]*([0-9]+\.?[0-9]*)"],
}

VITAL_PATTERNS = {
    "blood_pressure": [r"Blood Pressure[:\s]*([0-9]{2,3}/[0-9]{2,3})"],
    "heart_rate": [r"Heart Rate[:\s]*([0-9]{2,3})"],
    "temperature": [r"Temperature[:\s]*([0-9]+\.?[0-9]*)"],
    "oxygen_saturation": [r"SpO2[:\s]*([0-9]{2,3})"],
}

DISEASE_KEYWORDS = [
    "diabetes",
    "hypertension",
    "asthma",
    "pneumonia",
    "infection",
    "covid",
    "cancer",
]


def clean_text(value):
    if not value:
        return None
    return re.sub(r"\s+", " ", str(value)).strip()


def search_patterns(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return clean_text(match.group(1))
    return None


def parse_medications(text: str) -> List[Dict[str, Any]]:
    medications = []

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        med_match = re.search(
            r"([A-Za-z][A-Za-z0-9 ]+)\s+(\d+\s*(mg|ml|mcg|g))",
            line,
            re.I,
        )

        if med_match:
            medications.append(
                {
                    "drug_name": clean_text(med_match.group(1)),
                    "dosage": clean_text(med_match.group(2)),
                    "frequency": None,
                    "duration": None,
                    "raw_text": line,
                }
            )

    return medications


def find_disease(text):
    for disease in DISEASE_KEYWORDS:
        if disease.lower() in text.lower():
            return disease
    return None


def parse_medical_entities(text: str) -> Dict[str, Any]:
    extracted = {}

    for key, patterns in LABEL_PATTERNS.items():
        extracted[key] = search_patterns(text, patterns)

    for key, patterns in VITAL_PATTERNS.items():
        extracted[key] = search_patterns(text, patterns)

    for key, patterns in LAB_PATTERNS.items():
        extracted[key] = search_patterns(text, patterns)

    extracted["disease"] = find_disease(text)
    extracted["medications"] = parse_medications(text)

    return extracted


def generate_summary(extracted: Dict[str, Any]) -> str:
    summary = []

    if extracted.get("patient_name"):
        summary.append(
            f"Patient Name: {extracted['patient_name']}"
        )

    if extracted.get("disease"):
        summary.append(
            f"Detected Disease: {extracted['disease']}"
        )

    if extracted.get("medications"):
        meds = ", ".join(
            [
                m["drug_name"]
                for m in extracted["medications"]
                if m.get("drug_name")
            ]
        )

        summary.append(
            f"Medications: {meds}"
        )

    if not summary:
        summary.append(
            "Medical document processed successfully."
        )

    return ". ".join(summary)


def answer_question(
    extracted: Dict[str, Any],
    question: str,
) -> str:

    q = question.lower()

    if "disease" in q:
        return extracted.get(
            "disease",
            "No disease information found.",
        )

    if "medicine" in q or "drug" in q:
        meds = extracted.get("medications", [])

        if meds:
            return ", ".join(
                [m["drug_name"] for m in meds]
            )

        return "No medication information found."

    if "patient" in q:
        return extracted.get(
            "patient_name",
            "Patient name not found.",
        )

    return "Information not available in uploaded document."