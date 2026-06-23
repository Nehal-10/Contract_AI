from pathlib import Path
import pandas as pd
import pickle

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# LOAD DATA
# ==========================================

dataset_file = (
    PROJECT_ROOT /
    "data" /
    "training" /
    "contract_training_dataset.csv"
)

df = pd.read_csv(dataset_file)

print(
    f"Samples: {len(df)}"
)

# ==========================================
# TEXT
# ==========================================

X_text = (
    df["text"]
    .fillna("")
    .astype(str)
)

y = df["contract_type"]

# ==========================================
# EMBEDDINGS
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("\nGenerating embeddings...")

X = model.encode(
    X_text.tolist(),
    show_progress_bar=True
)

print(
    f"Embedding Shape: {X.shape}"
)

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# MODEL
# ==========================================

classifier = LogisticRegression(
    max_iter=2000
)

classifier.fit(
    X_train,
    y_train
)

# ==========================================
# EVALUATION
# ==========================================

predictions = classifier.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nAccuracy:")
print(accuracy)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# ==========================================
# SAVE MODEL
# ==========================================

model_file = (
    PROJECT_ROOT /
    "models" /
    "contract_type_classifier.pkl"
)

with open(
    model_file,
    "wb"
) as f:

    pickle.dump(
        classifier,
        f
    )

print("\nSaved Model:")
print(model_file)