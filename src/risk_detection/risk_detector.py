from pathlib import Path
import pandas as pd

from risk_rules import RISK_RULES

PROJECT_ROOT = Path(__file__).resolve().parents[2]

csv_path = PROJECT_ROOT / "data" / "processed" / "all_clauses.csv"

df = pd.read_csv(csv_path)

total_score = 0

findings = []

for _, row in df.iterrows():

    text = str(row["text"]).lower()

    for risk_name, config in RISK_RULES.items():

        for keyword in config["keywords"]:

            if keyword in text:

                findings.append(
                    {
                        "risk": risk_name,
                        "level": config["level"],
                        "score": config["score"],
                        "title": row["title"]
                    }
                )

                total_score += config["score"]

                break

print("\nDetected Risks:\n")

for item in findings:

    print(
        f"{item['risk']} | "
        f"{item['level']} | "
        f"+{item['score']} | "
        f"{item['title']}"
    )

print("\nTotal Risk Score:", total_score)