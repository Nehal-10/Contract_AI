from pathlib import Path
import pandas as pd


from risk_detection.risk_detector_v2 import (
    detect_risks
)

from compliance.compliance_detector_v2 import (
    detect_compliance
)

from scoring.risk_scoring import (
    calculate_score
)
from src.classification.contract_classifier import (
    classify_contract
)

# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# MAIN PIPELINE
# ==========================================

def analyze_contract():

    print("\n")
    print("=" * 80)
    print("CONTRACT ANALYSIS STARTED")
    print("=" * 80)

    # ======================================
    # LOAD CLAUSES
    # ======================================

    clauses_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "all_clauses.csv"
    )

    clauses_df = pd.read_csv(
        clauses_file
    )

    print(
        f"\nClauses Loaded: {len(clauses_df)}"
    )

    # ======================================
    # CONTRACT TYPE
    # ======================================

    # Temporary
    # We will connect your trained
    # contract classifier later

   # ======================================
# CONTRACT TYPE
# ======================================

    combined_text = " ".join(
        clauses_df["text"]
        .fillna("")
        .astype(str)
     .tolist()
    )

    contract_type = classify_contract(
        combined_text
    )

    print(
        f"\nContract Type: {contract_type}"
    )
    # ======================================
    # RISK DETECTION
    # ======================================

    print("\nRunning Risk Detection...")

    risk_df = detect_risks(
        clauses_df
    )

    print(
        f"Risks Found: {len(risk_df)}"
    )

    # ======================================
    # COMPLIANCE
    # ======================================

    print(
        "\nRunning Compliance Check..."
    )

    compliance_df = detect_compliance(
        clauses_df
    )

    missing_count = len(

        compliance_df[
            compliance_df["status"]
            == "MISSING"
        ]

    )

    print(
        f"Missing Compliance Items: "
        f"{missing_count}"
    )

    # ======================================
    # SCORING
    # ======================================

    print(
        "\nCalculating Risk Score..."
    )

    report = calculate_score(
        risk_df,
        compliance_df
    )

    # ======================================
    # FINAL RESULT
    # ======================================

    result = {

        "contract_type":
            contract_type,

        "risk_score":
            report["risk_score"],

        "risk_level":
            report["risk_level"],

        "unique_risk_types":
            report["unique_risk_types"],

        "missing_compliance_items":
            report[
                "missing_compliance_items"
            ],

        "risk_penalty":
            report["risk_penalty"],

        "compliance_penalty":
            report[
                "compliance_penalty"
            ],

        "risk_findings":
            risk_df[
                "risk_type"
            ].dropna()
             .unique()
             .tolist(),

        "missing_requirements":
            compliance_df[
                compliance_df["status"]
                == "MISSING"
            ]["requirement"]
             .tolist()
    }

    # ======================================
    # SAVE JSON-LIKE REPORT CSV
    # ======================================

    output_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "pipeline_report.csv"
    )

    pd.DataFrame(
        [result]
    ).to_csv(
        output_file,
        index=False
    )

    print("\n")
    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    print("\nSaved:")
    print(output_file)

    return result


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    analyze_contract()