from pathlib import Path
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

csv_path = PROJECT_ROOT / "data" / "processed" / "all_clauses.csv"

df = pd.read_csv(csv_path)

print("Total Clauses:", len(df))

# --------------------------------------------------
# Create Embeddings
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    df["text"].fillna("").tolist(),
    show_progress_bar=True
)

print("Embeddings Shape:", embeddings.shape)

# --------------------------------------------------
# KMeans Clustering
# --------------------------------------------------

NUM_CLUSTERS = 10

kmeans = KMeans(
    n_clusters=NUM_CLUSTERS,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(embeddings)

df["cluster"] = clusters

# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_path = PROJECT_ROOT / "data" / "processed" / "clustered_clauses.csv"

df.to_csv(output_path, index=False)

print("\nSaved:")
print(output_path)