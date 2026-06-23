import re
import pandas as pd


def segment_clauses(text):

    lines = text.split("\n")

    clauses = []

    current_title = None
    current_text = []

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if re.match(r"^\d+\.?$", line):

            j = i + 1

            while j < len(lines):

                candidate = lines[j].strip()

                if candidate:

                    break

                j += 1

            if (
                j < len(lines)
                and len(candidate) > 3
                and len(candidate) < 80
                and "NDA Rev" not in candidate
                and "Form NDA" not in candidate
            ):

                if current_title:

                    clauses.append({
                        "title": current_title,
                        "text": " ".join(current_text)
                    })

                current_title = candidate
                current_text = []

                i = j + 1
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