from pathlib import Path
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLAUSES_FILE = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

RISK_FILE = (
    PROJECT_ROOT /
    "data" /
    "risk_library" /
    "high_risk_clauses.csv"
)


def detect_risks(clauses_df=None):

    if clauses_df is None:

        clauses_df = pd.read_csv(
            CLAUSES_FILE
        )
    risk_df = pd.read_csv(RISK_FILE)

    print(f"Total Clauses: {len(clauses_df)}")
    print(f"Risk Library Size: {len(risk_df)}")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    contract_embeddings = model.encode(
        clauses_df["text"].fillna("").tolist(),
        show_progress_bar=True
    )

    risk_embeddings = model.encode(
        risk_df["clause"].fillna("").tolist(),
        show_progress_bar=True
    )

    SIMILARITY_THRESHOLD = 0.68

    results = []

    for clause_idx, clause_embedding in enumerate(contract_embeddings):

        similarities = cosine_similarity(
            [clause_embedding],
            risk_embeddings
        )[0]

        best_match_idx = similarities.argmax()

        best_score = similarities[best_match_idx]

        if best_score >= SIMILARITY_THRESHOLD:

            risk_type = risk_df.iloc[
                best_match_idx
            ]["risk_type"]

            title = clauses_df.iloc[
                clause_idx
            ]["title"]

            matched_clause = risk_df.iloc[
                best_match_idx
            ]["clause"]

            results.append({
                "title": title,
                "risk_type": risk_type,
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
        "risk_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    return results_df


if __name__ == "__main__":
    clauses_df = pd.read_csv(
        CLAUSES_FILE
    )
    results_df = detect_risks(
        clauses_df
    )

    print("\n")
    print("=" * 80)
    print("RISK DETECTION RESULTS")
    print("=" * 80)

    for _, row in results_df.iterrows():

        print(
            f"\nRisk: {row['risk_type']}"
        )

        print(
            f"Similarity: {row['similarity']}"
        )

        print(
            f"Clause: {row['title']}"
        )

        print(
            f"Matched Risk Example: "
            f"{row['matched_clause']}"
        )

    print("\n")
    print("=" * 80)
    print(
        f"Total Risks Found: {len(results_df)}"
    )