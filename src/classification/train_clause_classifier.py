from pathlib import Path
import pandas as pd
import joblib

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -----------------------------------
# Load dataset
# -----------------------------------

df = pd.read_csv(
    PROJECT_ROOT /
    "data" /
    "training" /
    "training_dataset.csv"
)

print("Samples:", len(df))

# -----------------------------------
# Text + Labels
# -----------------------------------

X_text = df["text"].astype(str)

y = df["category"]

# -----------------------------------
# Embeddings
# -----------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("\nGenerating embeddings...")

X = model.encode(
    X_text.tolist(),
    show_progress_bar=True
)

print("Embedding Shape:", X.shape)

# -----------------------------------
# Train Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------------
# Train Classifier
# -----------------------------------

clf = LogisticRegression(
    max_iter=2000
)

clf.fit(
    X_train,
    y_train
)

# -----------------------------------
# Evaluate
# -----------------------------------

preds = clf.predict(X_test)

print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        preds
    )
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        preds
    )
)

# -----------------------------------
# Save Model
# -----------------------------------

model_dir = (
    PROJECT_ROOT /
    "models"
)

model_dir.mkdir(
    exist_ok=True
)

joblib.dump(
    clf,
    model_dir /
    "clause_classifier.pkl"
)

print("\nSaved Model:")
print(
    model_dir /
    "clause_classifier.pkl"
)