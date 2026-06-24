from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# SEVERITY WEIGHTS
# ==========================================

SEVERITY_WEIGHTS = {
    "LOW": 5,
    "MEDIUM": 10,
    "HIGH": 20
}

# ==========================================
# COMPLIANCE WEIGHTS
# ==========================================

COMPLIANCE_WEIGHTS = {

    # NDA
    "Definition Of Confidential Information": 10,
    "Confidentiality Obligations": 15,
    "Permitted Disclosures": 10,
    "Return Or Destruction Of Information": 15,
    "Term Of Confidentiality": 10,
    "Governing Law": 10,

    # Employment
    "Job Duties": 10,
    "Compensation": 15,
    "Termination": 15,
    "Confidentiality": 10,
    "Non Compete": 10,

    # MSA
    "Scope Of Services": 10,
    "Payment Terms": 15,
    "Limitation Of Liability": 15,
    "Termination Clause": 10,
    "Dispute Resolution": 10,

    # Vendor
    "Goods Or Services": 10,
    "Pricing": 15,
    "Delivery Terms": 10
}

# ==========================================
# MAIN FUNCTION
# ==========================================

def calculate_score(
    risk_df,
    compliance_df
):

    # ======================================
    # RISK PENALTY
    # ======================================

    risk_penalty = 0

    if (
        risk_df is not None
        and not risk_df.empty
    ):

        unique_risks = (
            risk_df["risk_type"]
            .dropna()
            .unique()
        )

        for _, row in risk_df.iterrows():

            severity = str(
                row.get(
                    "severity",
                    "MEDIUM"
                )
            ).upper()

            risk_penalty += (
                SEVERITY_WEIGHTS.get(
                    severity,
                    10
                )
            )

    else:

        unique_risks = []

    # ======================================
    # COMPLIANCE PENALTY
    # ======================================

    missing_requirements = compliance_df[
        compliance_df["status"] == "MISSING"
    ]

    compliance_penalty = 0

    for _, row in missing_requirements.iterrows():

        compliance_penalty += (
            COMPLIANCE_WEIGHTS.get(
                row["requirement"],
                10
            )
        )

    # ======================================
    # WEIGHTED PENALTY
    # ======================================

    weighted_penalty = (

        (risk_penalty * 0.60)

        +

        (compliance_penalty * 0.40)

    )

    weighted_penalty = min(
        weighted_penalty,
        100
    )

    # ======================================
    # FINAL SCORE
    # ======================================

    final_score = (
        100 - weighted_penalty
    )

    final_score = max(
        final_score,
        0
    )

    # ======================================
    # RISK LEVEL
    # ======================================

    if final_score >= 80:

        risk_level = "LOW"

    elif final_score >= 50:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # ======================================
    # REPORT
    # ======================================

    report = {

        "risk_score":
            round(
                final_score,
                2
            ),

        "risk_level":
            risk_level,

        "safety_score":
            round(
                final_score,
                2
            ),

        "unique_risk_types":
            len(
                unique_risks
            ),

        "missing_compliance_items":
            len(
                missing_requirements
            ),

        "risk_penalty":
            risk_penalty,

        "compliance_penalty":
            compliance_penalty,

        "weighted_penalty":
            round(
                weighted_penalty,
                2
            )
    }

    return report


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    risk_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "risk_results.csv"
    )

    compliance_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "compliance_report_v2.csv"
    )

    risk_df = pd.read_csv(
        risk_file
    )

    compliance_df = pd.read_csv(
        compliance_file
    )

    report = calculate_score(
        risk_df,
        compliance_df
    )

    print("\n")
    print("=" * 70)
    print("FINAL CONTRACT REPORT")
    print("=" * 70)

    for key, value in report.items():

        print(
            f"{key}: {value}"
        )

    report_df = pd.DataFrame(
        [report]
    )

    output_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "final_contract_report.csv"
    )

    report_df.to_csv(
        output_file,
        index=False
    )

    print("\nSaved:")
    print(output_file)