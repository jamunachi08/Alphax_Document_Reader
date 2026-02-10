import frappe
from frappe.model.document import Document
from alphax_document_reader.utils.extractors import extract_text_from_file_url

class AlphaXDocument(Document):

    @frappe.whitelist()
    def extract_text(self):
        """
        Extract text from the attached file and store it in this document.
        Supports: PDF, images, DOCX, TXT, CSV, XLSX.
        """
        if not self.file:
            frappe.throw("Please attach a file first.")

        self.status = "Processing"
        self.save(ignore_permissions=True)

        try:
            result = extract_text_from_file_url(self.file)
            self.file_type = result.get("file_type") or self.file_type
            self.pages = result.get("pages") or 0
            self.extracted_text = result.get("text") or ""
            self.error = ""
            self.status = "Extracted"
            self.extracted_on = frappe.utils.now()
        except Exception as e:
            self.status = "Failed"
            self.error = frappe.get_traceback(with_context=True)

        self.save(ignore_permissions=True)
        return {"status": self.status}
