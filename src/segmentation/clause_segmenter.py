import pandas as pd
import re


def segment_clauses(text):

    lines = text.split("\n")

    clauses = []

    current_title = None
    current_text = []

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # =====================================
        # FORMAT 1:
        # 3. Onus.
        # 4. Remedies.
        # =====================================

        inline_match = re.match(
            r"^\s*(\d+)\.\s*(.+)",
            line
        )

        if inline_match:

            if current_title:

                clauses.append({
                    "title": current_title,
                    "text": " ".join(current_text)
                })

            current_title = (
                inline_match.group(2).strip()
            )

            current_text = []

            i += 1
            continue

        # =====================================
        # FORMAT 2:
        # 3.
        # Remedies.
        # =====================================

        if (
            line.replace(".", "").isdigit()
            and i + 1 < len(lines)
        ):

            next_line = lines[i + 1].strip()

            if (
                len(next_line) > 3
                and len(next_line) < 100
                and "NDA Rev" not in next_line
                and "Form NDA" not in next_line
            ):

                if current_title:

                    clauses.append({
                        "title": current_title,
                        "text": " ".join(current_text)
                    })

                current_title = next_line

                current_text = []

                i += 2
                continue

        if current_title:

            current_text.append(line)

        i += 1

    if current_title:

        clauses.append({
            "title": current_title,
            "text": " ".join(current_text)
        })

    return pd.DataFrame(clauses)