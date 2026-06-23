from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

titles = (
    df["title"]
    .dropna()
    .unique()
)

print("Total Unique Titles:")
print(len(titles))

print("\n")

for t in sorted(titles):
    print(t)