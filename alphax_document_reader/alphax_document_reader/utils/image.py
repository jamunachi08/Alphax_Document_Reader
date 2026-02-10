import io

def extract_image_text(content: bytes, force_ocr: bool = False) -> str:
    """Extract text from image. If OCR libs aren't installed, returns empty string."""
    if not force_ocr:
        return ""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(io.BytesIO(content))
        return (pytesseract.image_to_string(img) or "").strip()
    except Exception:
        return ""
