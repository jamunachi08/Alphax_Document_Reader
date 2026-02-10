# AlphaX Document Reader

AlphaX Document Reader is a Frappe/ERPNext app that lets you upload documents and extract text from them.

## Supported formats (built-in)
- PDF (text layer) via `pdfplumber`
- DOCX via `python-docx`
- TXT/MD/LOG/CSV (plain text)
- XLSX/XLS via `pandas` + `openpyxl`
- Images (PNG/JPG/WEBP/TIFF) **optional** OCR

## Optional OCR
Enable OCR in **AlphaX Doc Reader Settings** and install one of:
- `pytesseract` (requires system Tesseract)
- `easyocr` (pure python, heavier)
For scanned PDF OCR fallback, also install:
- `pdf2image` + poppler system package

## Usage
1. Install the app: `bench get-app` / `bench install-app alphax_document_reader`
2. Open **AlphaX Document** list → New → attach a file → click **Extract Text**.
3. Extracted text is stored in the document for downstream use (search, parsing, integrations).

## Branding
- App email: erpsupport@alphax.com
- Brand: alphaX

## Version
0.1.0 (2026-02-10)


## Desk Page
Open **Document Reader** desk page: `/app/document-reader`
