"""
Simplified OCR service that uses pytesseract instead of PaddleOCR
for easier local development without heavy ML dependencies.
"""
import io
from pathlib import Path
from PIL import Image

# Simple fallback when pytesseract is not available
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def save_upload_file(upload_bytes: bytes, filename: str, upload_dir: Path) -> str:
    upload_dir.mkdir(parents=True, exist_ok=True)
    target_path = upload_dir / filename
    with open(target_path, "wb") as out_file:
        out_file.write(upload_bytes)
    return str(target_path)


def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using pytesseract or mock data"""
    if TESSERACT_AVAILABLE:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Tesseract error: {e}")
            return generate_mock_medical_text()
    else:
        # Return mock medical record for testing
        return generate_mock_medical_text()


def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF - returns mock data for testing"""
    return generate_mock_medical_text()


def extract_text_from_path(path: str, content_type: str) -> str:
    """Main entry point for text extraction"""
    extension = Path(path).suffix.lower()
    
    if extension == ".pdf":
        return extract_text_from_pdf(path)
    else:
        return extract_text_from_image(path)


def generate_mock_medical_text() -> str:
    """Generate mock medical record for testing"""
    return """
    MEDICAL RECORD

    Patient Name: John Doe
    Patient ID: MRN12345
    Age: 45
    Gender: Male
    Date of Birth: 01/15/1979
    Blood Group: O+

    DIAGNOSIS
    Type 2 Diabetes Mellitus
    Hypertension

    VITAL SIGNS
    Blood Pressure: 140/90
    Heart Rate: 78
    Temperature: 98.6
    SpO2: 97

    LAB RESULTS
    Hemoglobin: 14.2 g/dL
    WBC: 7500
    RBC: 4.8
    Platelets: 250000
    Glucose: 180 mg/dL
    Cholesterol: 220 mg/dL

    MEDICATIONS
    Metformin 500mg twice daily
    Lisinopril 10mg once daily
    Aspirin 75mg once daily

    ALLERGIES
    No known drug allergies

    SYMPTOMS
    Increased thirst, frequent urination, fatigue

    MEDICAL HISTORY
    No significant past medical history
    No previous surgeries

    Dr. Jane Smith, MD
    Internal Medicine
    """
