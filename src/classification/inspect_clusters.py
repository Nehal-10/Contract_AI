from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "clustered_clauses.csv"
)

for cluster_id in sorted(df["cluster"].unique()):

    print("\n")
    print("=" * 80)
    print(f"CLUSTER {cluster_id}")
    print("=" * 80)

    cluster_df = df[df["cluster"] == cluster_id]

    for _, row in cluster_df.head(5).iterrows():
        print("\nTITLE:")
        print(row["title"])

        print("\nTEXT PREVIEW:")
        print(str(row["text"])[:200])

        print("-" * 50)