from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

clauses_df = pd.read_csv(
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

types_df = pd.read_csv(
    PROJECT_ROOT /
    "data" /
    "training" /
    "contract_types.csv"
)

merged = clauses_df.merge(
    types_df,
    on="contract_name"
)

print(merged[
    ["contract_name", "contract_type"]
].head())

output_file = (
    PROJECT_ROOT /
    "data" /
    "training" /
    "contract_training_dataset.csv"
)

merged.to_csv(
    output_file,
    index=False
)

print("\nSaved:")
print(output_file)