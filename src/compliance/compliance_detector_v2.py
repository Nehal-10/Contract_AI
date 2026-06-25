from pathlib import Path
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from src.models.embedding_model import model


SIMILARITY_THRESHOLD = 0.50

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def detect_compliance(
    clauses_df,
    contract_type
):

    clauses_df["text"] = (
        clauses_df["text"]
        .fillna("")
        .astype(str)
    )

    # =====================================
    # LOAD REQUIREMENTS BASED ON CONTRACT
    # =====================================

    if contract_type == "NDA":

        requirements_file = (
            PROJECT_ROOT /
            "data" /
            "compliance" /
            "nda_requirements.csv"
        )

    elif contract_type == "Employment":

        requirements_file = (
            PROJECT_ROOT /
            "data" /
            "compliance" /
            "employment_requirements.csv"
        )

    elif contract_type == "MSA":

        requirements_file = (
            PROJECT_ROOT /
            "data" /
            "compliance" /
            "msa_requirements.csv"
        )

    else:

        requirements_file = (
            PROJECT_ROOT /
            "data" /
            "compliance" /
            "vendor_requirements.csv"
        )

    # =====================================
    # READ FILE
    # =====================================

    requirements_df = pd.read_csv(
        requirements_file
    )

    print("\nLoaded Compliance File:")
    print(requirements_file)

    print("\nColumns:")
    print(
        requirements_df.columns.tolist()
    )

    # =====================================
    # VALIDATION
    # =====================================

    required_columns = [
        "requirement",
        "description",
        "keywords"
    ]

    for col in required_columns:

        if col not in requirements_df.columns:

            raise ValueError(
                f"Missing column '{col}' "
                f"in {requirements_file}"
            )

    print(
        f"\nTotal Clauses: {len(clauses_df)}"
    )

    print(
        f"Compliance Requirements: "
        f"{len(requirements_df)}"
    )

    # =====================================
    # EMBEDDINGS
    # =====================================

    clause_embeddings = model.encode(
        clauses_df["text"].tolist(),
        show_progress_bar=True
    )

    results = []

    # =====================================
    # CHECK EACH REQUIREMENT
    # =====================================

    for _, row in requirements_df.iterrows():

        requirement = row["requirement"]

        description = row["description"]

        keywords = str(
            row["keywords"]
        ).lower().split("|")

        requirement_embedding = model.encode(
            [description]
        )

        similarities = cosine_similarity(
            requirement_embedding,
            clause_embeddings
        )[0]

        best_idx = similarities.argmax()

        best_score = similarities[
            best_idx
        ]

        matched_clause = (
            clauses_df.iloc[
                best_idx
            ]["title"]
        )

        matched_text = str(
            clauses_df.iloc[
                best_idx
            ]["text"]
        ).lower()

        title_text = str(
            matched_clause
        ).lower()

        requirement_text = str(
            requirement
        ).lower()

        # ==============================
        # KEYWORD SCORE
        # ==============================

        keyword_hits = sum(

            1
            for keyword in keywords

            if keyword.strip()
            and keyword.strip()
            in matched_text

        )

        keyword_score = (

            keyword_hits
            /
            len(keywords)

            if len(keywords) > 0
            else 0

        )

        # ==============================
        # TITLE BOOST
        # ==============================

        title_boost = 0

        requirement_words = (
            requirement_text
            .replace("_", " ")
            .split()
        )

        for word in requirement_words:

            if len(word) > 4 and word in title_text:

                title_boost = 0.10
                break
       
        # ==============================
        # FINAL COMBINED SCORE
        # ==============================

        combined_score = (

            (best_score * 0.70)

            +

            (keyword_score * 0.20)

            +

            title_boost

        )

        # ==============================
        # TITLE BOOST
        # ==============================

        title_text = str(
            matched_clause
        ).lower()
        requirement_text = str(
            requirement
        ).lower()
        title_boost = 0
        for word in requirement_text.split():
            if word in title_text:
                title_boost = 0.10
                break
        # SPECIAL CASE
        if (
            "governing law" in requirement_text
            and
            "governing law" in title_text
            ):
            title_boost += 0.20
        # ==============================
        #  COMBINED SCORE
        #  ==============================
        combined_score = (
            (best_score * 0.60)
            +
            (keyword_score * 0.30)
            +
            title_boost
        )
        # ==============================
        #  HYBRID DECISION
        # ==============================
        if best_score >= 0.60:
            status = "FOUND"
        elif combined_score >= 0.55:
            status = "FOUND"
            
        elif keyword_score >= 0.75:
            status = "FOUND"
        else:
            status = "MISSING"
        # ==============================
        #  DEBUG OUTPUT
        #  ==============================
        print(
            f"{requirement} | "
            f"Semantic={best_score:.3f} | "
            f"Keyword={keyword_score:.3f} | "
            f"TitleBoost={title_boost:.2f} | "
            f"Combined={combined_score:.3f}"
        )

        # ==============================
        # STORE RESULT
        # ==============================

        results.append({

            "requirement":
                requirement,

            "status":
                status,

            "similarity":
                round(
                    float(best_score),
                    3
                ),

            "keyword_score":
                round(
                    float(keyword_score),
                    3
                ),

            "combined_score":
                round(
                    float(combined_score),
                    3
                ),

            "matched_clause":
                matched_clause

        })

    # =====================================
    # SAVE REPORT
    # =====================================

    results_df = pd.DataFrame(
        results
    )

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


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    clauses_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "all_clauses.csv"
    )

    clauses_df = pd.read_csv(
        clauses_file
    )

    results_df = detect_compliance(
        clauses_df,
        "NDA"
    )

    print("\n")
    print("=" * 80)
    print("COMPLIANCE REPORT")
    print("=" * 80)

    print(results_df)

    found_count = (

        results_df["status"]
        ==
        "FOUND"

    ).sum()

    score = (

        found_count
        /
        len(results_df)

    ) * 100

    print("\nCompliance Score:")
    print(f"{score:.2f}%")
