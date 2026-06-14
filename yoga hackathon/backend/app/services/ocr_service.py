import io
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

OCR_ENGINE = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)


def save_upload_file(upload_bytes: bytes, filename: str, upload_dir: Path) -> str:
    upload_dir.mkdir(parents=True, exist_ok=True)
    target_path = upload_dir / filename
    with open(target_path, "wb") as out_file:
        out_file.write(upload_bytes)
    return str(target_path)


def load_image_bytes(file_bytes: bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        image = np.array(Image.open(io.BytesIO(file_bytes)).convert("RGB"))
    return image


def extract_text_from_image(image):
    result = OCR_ENGINE.ocr(image, cls=True)
    lines = []
    if result and result[0]:
        for line in result[0]:
            if line and len(line) >= 2 and line[1]:
                lines.append(line[1][0])
    return "\n".join(lines)


def extract_text_from_pdf(path: str):
    pages = convert_from_path(path, dpi=220)
    text_lines = []
    for page in pages:
        image = cv2.cvtColor(np.asarray(page), cv2.COLOR_RGB2BGR)
        page_text = extract_text_from_image(image)
        if page_text:
            text_lines.append(page_text)
    return "\n".join(text_lines)


def extract_text_from_path(path: str, content_type: str):
    extension = Path(path).suffix.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(path)
    file_bytes = Path(path).read_bytes()
    image = load_image_bytes(file_bytes)
    return extract_text_from_image(image)
