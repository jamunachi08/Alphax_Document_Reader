import os
import io
import mimetypes
from pathlib import Path

import frappe

def _get_file_path(file_url: str) -> str:
    # file_url examples: /files/x.pdf or private/files/x.pdf
    file_doc = frappe.get_doc("File", {"file_url": file_url})
    return file_doc.get_full_path()

def extract_text_from_file_url(file_url: str) -> dict:
    path = _get_file_path(file_url)
    return extract_text_from_path(path)

def extract_text_from_path(path: str) -> dict:
    path = os.path.abspath(path)
    ext = (Path(path).suffix or "").lower().lstrip(".")
    mime, _ = mimetypes.guess_type(path)
    mime = mime or ""

    if ext in ("pdf",):
        return _extract_pdf(path)
    if ext in ("png","jpg","jpeg","webp","tif","tiff","bmp"):
        return _extract_image(path)
    if ext in ("docx",):
        return _extract_docx(path)
    if ext in ("txt", "log", "md", "csv"):
        return _extract_text_file(path, ext)
    if ext in ("xlsx","xls"):
        return _extract_excel(path)

    # fallback: try read as text
    return _extract_text_file(path, ext or "unknown")

def _extract_pdf(path: str) -> dict:
    import pdfplumber

    text_parts = []
    pages = 0
    with pdfplumber.open(path) as pdf:
        pages = len(pdf.pages)
        for p in pdf.pages:
            t = p.extract_text() or ""
            if t.strip():
                text_parts.append(t)

    text = "\n\n".join(text_parts).strip()

    # OCR fallback for scanned PDFs (optional)
    if not text:
        settings = frappe.get_single("AlphaX Doc Reader Settings")
        if settings.enable_pdf_ocr_fallback:
            try:
                text = _ocr_pdf(path)
            except Exception:
                # keep empty; caller will store traceback if needed
                pass

    return {"file_type": "pdf", "pages": pages, "text": text}

def _extract_image(path: str) -> dict:
    settings = frappe.get_single("AlphaX Doc Reader Settings")
    if not settings.enable_image_ocr:
        return {"file_type": "image", "pages": 1, "text": ""}

    return {"file_type": "image", "pages": 1, "text": _ocr_image(path)}

def _extract_docx(path: str) -> dict:
    from docx import Document
    doc = Document(path)
    paras = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return {"file_type": "docx", "pages": 0, "text": "\n".join(paras).strip()}

def _extract_text_file(path: str, ext: str) -> dict:
    # csv is handled as plain text unless you prefer tabular
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return {"file_type": ext, "pages": 0, "text": f.read().strip()}

def _extract_excel(path: str) -> dict:
    import pandas as pd

    xls = pd.ExcelFile(path)
    parts = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        parts.append(f"## Sheet: {sheet}\n{df.to_csv(index=False)}")
    return {"file_type": "excel", "pages": 0, "text": "\n\n".join(parts).strip()}

def _ocr_image(path: str) -> str:
    # Prefer pytesseract if available; otherwise try easyocr.
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        try:
            import easyocr
            reader = easyocr.Reader(['en','ar'], gpu=False)
            result = reader.readtext(path, detail=0)
            return "\n".join(result)
        except Exception as e:
            raise

def _ocr_pdf(path: str) -> str:
    # Simple implementation: render pages to images and OCR.
    # Requires 'pytesseract' + a PDF renderer (poppler via pdf2image), or easyocr.
    try:
        from pdf2image import convert_from_path
    except Exception:
        raise RuntimeError("pdf2image is required for PDF OCR fallback. Install pdf2image and poppler utilities on the server.")

    images = convert_from_path(path, dpi=250)
    texts = []
    for img in images:
        try:
            import pytesseract
            texts.append(pytesseract.image_to_string(img))
        except Exception:
            # easyocr path
            import easyocr, numpy as np
            reader = easyocr.Reader(['en','ar'], gpu=False)
            texts.extend(reader.readtext(np.array(img), detail=0))
    return "\n\n".join([t for t in texts if t and t.strip()]).strip()
