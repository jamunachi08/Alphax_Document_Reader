import frappe

@frappe.whitelist()
def extract_document(docname: str):
    doc = frappe.get_doc("AlphaX Document", docname)
    return doc.extract_text()

@frappe.whitelist()
def create_and_extract(file_url: str, title: str = None, reference_doctype: str = None, reference_name: str = None):
    doc = frappe.get_doc({
        "doctype": "AlphaX Document",
        "title": title or (file_url.split('/')[-1] if file_url else "Document"),
        "file": file_url,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "status": "Queued",
    })
    doc.insert(ignore_permissions=True)
    doc.extract_text()
    return {"name": doc.name, "status": doc.status}
