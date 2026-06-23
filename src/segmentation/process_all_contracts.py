from pathlib import Path
import fitz
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

contracts_folder = PROJECT_ROOT / "data" / "contracts"

all_data = []

pdf_files = list(contracts_folder.glob("*.pdf"))

print(f"Found {len(pdf_files)} contracts")

for pdf_file in pdf_files:

    print(f"Processing {pdf_file.name}")

    doc = fitz.open(pdf_file)

    text = ""

    for page in doc:
        text += page.get_text()

    pattern = r"\n\s*(\d+)\.\s*\n"

    matches = list(re.finditer(pattern, text))

    for i in range(len(matches)):

        clause_number = matches[i].group(1)

        start = matches[i].start()

        if i < len(matches)-1:
            end = matches[i+1].start()
        else:
            end = len(text)

        clause_text = text[start:end].strip()

        lines = clause_text.split("\n")

        title = ""

        if len(lines) > 1:
            title = lines[1].strip()

        all_data.append({
            "contract_name": pdf_file.name,
            "clause_number": clause_number,
            "title": title,
            "text": clause_text
        })

df = pd.DataFrame(all_data)

print(df.head())

print(f"\nTotal Clauses: {len(df)}")

output_path = PROJECT_ROOT / "data" / "processed" / "all_clauses.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved to: {output_path}")