from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# RISK WEIGHTS
# ==========================================

RISK_WEIGHTS = {

    "Unlimited Liability": 20,

    "Broad Indemnity": 15,

    "One Sided Termination": 15,

    "Auto Renewal": 10,

    "Confidentiality Forever": 10,

    "No Audit Rights": 10,

    "No Data Protection": 15,

    "Weak Security Controls": 15
}

# ==========================================
# COMPLIANCE WEIGHTS
# ==========================================

COMPLIANCE_WEIGHTS = {

    "Consent": 10,

    "Data Retention": 15,

    "Right To Deletion": 15,

    "Data Processing": 10,

    "Data Security": 20,

    "Data Transfer": 10
}

# ==========================================
# MAIN FUNCTION
# ==========================================

def calculate_score(
    risk_df,
    compliance_df
):

    risk_score = 0

    unique_risks = (
        risk_df["risk_type"]
        .dropna()
        .unique()
    )

    for risk_type in unique_risks:

        risk_score += RISK_WEIGHTS.get(
            risk_type,
            10
        )

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

    total_penalty = (
    risk_score +
    compliance_penalty
    )

    total_penalty = min(
    total_penalty,
    100
    )

    final_score = 100 - total_penalty
    if final_score >= 80:

        risk_level = "LOW"

    elif final_score >= 50:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    return {

        "risk_score":
            final_score,

        "risk_level":
            risk_level,

        "safety_score":
            100 - final_score,

        "unique_risk_types":
            len(unique_risks),

        "missing_compliance_items":
            len(missing_requirements),

        "risk_penalty":
            risk_score,

        "compliance_penalty":
            compliance_penalty
    }


# ==========================================
# TEST MODE
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