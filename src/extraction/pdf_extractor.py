from pathlib import Path

import fitz


def extract_pdf_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:

        text += page.get_text()

    doc.close()

    return text


if __name__ == "__main__":

    pdf_file = Path(
        "data/contracts/NondisclosureAgreement.pdf"
    )

    extracted_text = extract_pdf_text(
        pdf_file
    )

    print(
        extracted_text[:2000]
    )