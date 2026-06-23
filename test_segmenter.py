from src.extraction.pdf_extractor import extract_pdf_text
from src.segmentation.clause_segmenter import segment_clauses

pdf_path = "data/contracts/NondisclosureAgreement.pdf"

text = extract_pdf_text(pdf_path)

clauses_df = segment_clauses(text)

print(clauses_df[["title"]])

print("\nTotal Clauses:")
print(len(clauses_df))