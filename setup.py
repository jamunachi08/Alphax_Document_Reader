from setuptools import setup, find_packages

# Bench / Frappe still supports setup.py based apps.
setup(
    name="alphax_document_reader",
    version="0.1.0",
    description="AlphaX Document Reader",
    author="AlphaX",
    author_email="erpsupport@alphax.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pdfplumber",
        "pdfminer-six",
        "pandas",
        "openpyxl>=3.1.0",
        "python-docx",
        "Pillow",
    ],
)
