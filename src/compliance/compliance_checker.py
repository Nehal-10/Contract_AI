from pathlib import Path
import pandas as pd

# ==========================
# GDPR REQUIREMENTS
# ==========================

GDPR_REQUIREMENTS = {
    "Consent": [
        "consent",
        "user consent",
        "customer consent",
        "permission to process"
    ],

    "Data Retention": [
        "data retention",
        "retain data",
        "retention period",
        "storage period"
    ],

    "Right To Deletion": [
        "delete data",
        "right to deletion",
        "erase data",
        "right to erasure"
    ],

    "Data Processing": [
        "data processing",
        "process personal data",
        "processing personal information"
    ]
}


# ==========================
# PROJECT ROOT
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================
# LOAD CLAUSES
# ==========================

clauses_file = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "all_clauses.csv"
)

df = pd.read_csv(clauses_file)

print(f"\nTotal Clauses Loaded: {len(df)}")

# ==========================
# MERGE ALL CLAUSE TEXT
# ==========================

all_text = " ".join(
    df["text"].fillna("").astype(str)
).lower()

# ==========================
# COMPLIANCE CHECK
# ==========================

found = []
missing = []

for requirement, keywords in GDPR_REQUIREMENTS.items():

    exists = False

    for keyword in keywords:

        if keyword.lower() in all_text:
            exists = True
            break

    if exists:
        found.append(requirement)
    else:
        missing.append(requirement)

# ==========================
# COMPLIANCE SCORE
# ==========================

total_requirements = len(GDPR_REQUIREMENTS)

score = (
    len(found) / total_requirements
) * 100

# ==========================
# PRINT REPORT
# ==========================

print("\n" + "=" * 70)
print("COMPLIANCE REPORT")
print("=" * 70)

print("\nFOUND REQUIREMENTS:\n")

for item in found:
    print(f"✓ {item}")

print("\nMISSING REQUIREMENTS:\n")

for item in missing:
    print(f"✗ {item}")

print(f"\nCompliance Score: {score:.2f}%")

# ==========================
# SAVE REPORT
# ==========================

report = []

for item in found:
    report.append({
        "requirement": item,
        "status": "FOUND"
    })

for item in missing:
    report.append({
        "requirement": item,
        "status": "MISSING"
    })

report_df = pd.DataFrame(report)

output_file = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "compliance_report.csv"
)

report_df.to_csv(
    output_file,
    index=False
)

print("\nSaved Report:")
print(output_file)

print("\n" + "=" * 70)
print("COMPLIANCE CHECK COMPLETE")
print("=" * 70)