import pdfplumber as pdp

def pdf_extract(file):
    text = ""

    try:
        with pdp.open(file) as pdf:

            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            if not text.strip():
                return None
            return text.strip()

    except Exception as e:
        return None