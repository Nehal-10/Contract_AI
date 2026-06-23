from pathlib import Path
import joblib

from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# load classifier
clf = joblib.load(
    PROJECT_ROOT /
    "models" /
    "clause_classifier.pkl"
)

# load embedding model
embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# sample clause
clause = """
The employee shall not disclose any confidential
information belonging to the company.
"""

embedding = embedder.encode([clause])

prediction = clf.predict(embedding)

print("\nPredicted Category:")
print(prediction[0])