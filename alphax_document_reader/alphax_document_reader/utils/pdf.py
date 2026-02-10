import io

def extract_pdf_text(content: bytes, force_ocr: bool = False) -> str:
    """Extract text from PDF. OCR is not implemented by default to keep cloud installs simple."""
    import pdfplumber
    out = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            if txt.strip():
                out.append(txt)
    return "\n\n".join(out).strip()
