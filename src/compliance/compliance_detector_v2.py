from pathlib import Path
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.60

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLAUSES_FILE = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

REQUIREMENTS_FILE = (
    PROJECT_ROOT /
    "data" /
    "compliance_requirements.csv"
)


def detect_compliance(clauses_df = None):
    if clauses_df is None:

        clauses_df = pd.read_csv(
            CLAUSES_FILE
        )
    
    clauses_df["text"] = (
        clauses_df["text"]
        .fillna("")
        .astype(str)
    )

    requirements_df = pd.read_csv(
        REQUIREMENTS_FILE
    )

    print(
        f"\nTotal Clauses: {len(clauses_df)}"
    )

    print(
        f"Compliance Requirements: {len(requirements_df)}"
    )

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    clause_embeddings = model.encode(
        clauses_df["text"].tolist(),
        show_progress_bar=True
    )

    results = []

    for _, row in requirements_df.iterrows():

        requirement = row["requirement"]
        description = row["description"]

        requirement_embedding = model.encode(
            [description]
        )

        similarities = cosine_similarity(
            requirement_embedding,
            clause_embeddings
        )[0]

        best_idx = similarities.argmax()

        best_score = similarities[best_idx]

        matched_clause = clauses_df.iloc[
            best_idx
        ]["title"]

        status = (
            "FOUND"
            if best_score >= SIMILARITY_THRESHOLD
            else "MISSING"
        )

        results.append({
            "requirement": requirement,
            "status": status,
            "similarity": round(
                float(best_score),
                3
            ),
            "matched_clause": matched_clause
        })

    results_df = pd.DataFrame(results)

    output_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "compliance_report_v2.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    return results_df


if __name__ == "__main__":

    results_df = detect_compliance()

    print("\n")
    print("=" * 80)
    print("SEMANTIC COMPLIANCE REPORT")
    print("=" * 80)

    for _, row in results_df.iterrows():

        print(
            "\nRequirement:",
            row["requirement"]
        )

        print(
            "Status:",
            row["status"]
        )

        print(
            "Similarity:",
            row["similarity"]
        )

        print(
            "Matched Clause:",
            row["matched_clause"]
        )

    found_count = (
        results_df["status"] == "FOUND"
    ).sum()

    score = (
        found_count /
        len(results_df)
    ) * 100

    print("\n")
    print("=" * 80)
    print(
        f"Compliance Score: {score:.2f}%"
    )
    print("=" * 80)