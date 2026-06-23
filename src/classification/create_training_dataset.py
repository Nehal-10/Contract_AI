from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -----------------------------
# Load all clauses
# -----------------------------
clauses_df = pd.read_csv(
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

# -----------------------------
# Load manual labels
# -----------------------------
labels_df = pd.read_excel(
    PROJECT_ROOT /
    "data" /
    "training" /
    "clause_labels.xlsx"
)

# -----------------------------
# Clean text
# -----------------------------
clauses_df["title"] = (
    clauses_df["title"]
    .astype(str)
    .str.strip()
)

labels_df["title"] = (
    labels_df["title"]
    .astype(str)
    .str.strip()
)

# -----------------------------
# Merge labels
# -----------------------------
training_df = clauses_df.merge(
    labels_df,
    on="title",
    how="inner"
)

# -----------------------------
# Keep required columns
# -----------------------------
training_df = training_df[
    [
        "title",
        "text",
        "category"
    ]
]

# -----------------------------
# Save
# -----------------------------
output_path = (
    PROJECT_ROOT /
    "data" /
    "training" /
    "training_dataset.csv"
)

training_df.to_csv(
    output_path,
    index=False
)

print("\nTraining Samples:", len(training_df))

print("\nCategory Distribution:")
print(
    training_df["category"]
    .value_counts()
)

print("\nSaved:")
print(output_path)