import frappe
from frappe import _
from .utils.extract import extract_text_from_file

@frappe.whitelist()
def extract_text(file_url: str = "", file_name: str = "", force_ocr: int = 0):
    """Extract plain text from a File URL or file name.

    Args:
        file_url: like /files/sample.pdf or /private/files/sample.pdf
        file_name: optional File.name / file_name
        force_ocr: 1 to force OCR for images/scanned PDFs where supported
    Returns:
        dict: {ok, text, meta}
    """
    if not file_url and not file_name:
        frappe.throw(_("file_url or file_name is required"))

    text, meta = extract_text_from_file(file_url=file_url, file_name=file_name, force_ocr=bool(int(force_ocr)))
    return {"ok": True, "text": text or "", "meta": meta or {}}
