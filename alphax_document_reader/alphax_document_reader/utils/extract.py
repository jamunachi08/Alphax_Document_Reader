import os
import io
import frappe
from frappe.utils.file_manager import get_file

def _guess_ext(file_path: str) -> str:
    _, ext = os.path.splitext((file_path or "").lower())
    return ext.lstrip(".")

def extract_text_from_file(file_url: str = "", file_name: str = "", force_ocr: bool = False):
    """Return (text, meta) from a file in File doctype."""
    fdoc = None
    if file_name:
        fdoc = frappe.get_doc("File", file_name)
        file_url = fdoc.file_url
    if not file_url:
        return "", {"reason": "missing_file_url"}

    # get_file returns (file_name, content)
    fname, content = get_file(file_url)
    ext = _guess_ext(fname)

    meta = {"file_name": fname, "ext": ext, "force_ocr": bool(force_ocr)}

    if ext in ("pdf",):
        from .pdf import extract_pdf_text
        return extract_pdf_text(content, force_ocr=force_ocr), meta

    if ext in ("png", "jpg", "jpeg", "webp", "tif", "tiff"):
        from .image import extract_image_text
        return extract_image_text(content, force_ocr=force_ocr), meta

    if ext in ("docx",):
        from .office import extract_docx_text
        return extract_docx_text(content), meta

    if ext in ("xlsx", "xlsm", "xls"):
        from .sheet import extract_sheet_text
        return extract_sheet_text(content), meta

    # Fallback: try decode as text
    try:
        return content.decode("utf-8", errors="ignore"), meta
    except Exception:
        return "", {**meta, "reason": "unsupported_type"}
