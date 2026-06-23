from src.extraction.pdf_extractor import extract_pdf_text

from src.classification.contract_classifier import (
    classify_contract
)

pdf_path = "data/contracts/NondisclosureAgreement.pdf"

text = extract_pdf_text(
    pdf_path
)

contract_type = classify_contract(
    text
)

print(contract_type)