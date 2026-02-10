import io

def extract_docx_text(content: bytes) -> str:
    import docx
    doc = docx.Document(io.BytesIO(content))
    paras = [p.text for p in doc.paragraphs if (p.text or "").strip()]
    return "\n".join(paras).strip()
