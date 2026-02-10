import io

def extract_sheet_text(content: bytes) -> str:
    import pandas as pd
    xls = pd.ExcelFile(io.BytesIO(content))
    parts = []
    for sheet in xls.sheet_names[:10]:  # guard
        df = xls.parse(sheet)
        parts.append(f"## {sheet}\n" + df.to_string(index=False))
    return "\n\n".join(parts).strip()
