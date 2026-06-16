import fitz

pdf_path = "data/contracts/nda.pdf"

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()

with open("contract_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Text saved successfully")