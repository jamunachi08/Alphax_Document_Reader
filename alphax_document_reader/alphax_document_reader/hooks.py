app_name = "alphax_document_reader"
app_title = "AlphaX Document Reader"
app_publisher = "AlphaX"
app_description = "Ingest & extract text from PDF/images/Office docs/spreadsheets; optional OCR/LLM parsing."
app_email = "erpsupport@alphax.com"
app_license = "mit"

# Assets
app_include_js = [
  "/assets/alphax_document_reader/js/alphax_doc_reader.js",
]
app_include_css = [
  "/assets/alphax_document_reader/css/alphax_doc_reader.css",
]

# Standard module
app_icon = "octicon octicon-file"
app_color = "green"
app_version = "0.1.0"
app_logo_url = "/assets/alphax_document_reader/images/alphax.svg"

# Fixtures: keep namespaced so you can export/import safely
fixtures = [
  {"dt": "Custom Field", "filters": [["name", "like", "AlphaX Document Reader%"]]},
  {"dt": "Property Setter", "filters": [["name", "like", "AlphaX Document Reader%"]]},
  {"dt": "Client Script", "filters": [["name", "like", "AlphaX Document Reader%"]]},
  {"dt": "Server Script", "filters": [["name", "like", "AlphaX Document Reader%"]]},
  {"dt": "Workspace", "filters": [["name", "in", ["AlphaX Document Reader"]]]},
]

# Optional: add a basic permission role
# after_install = "alphax_document_reader.install.after_install"

