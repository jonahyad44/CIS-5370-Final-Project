
import pandas as pd
from pathlib import Path

# Load the eligibility review CSV
file_path = Path("results/healthcare_eligibility_review.csv")

df = pd.read_csv(
    file_path,
    keep_default_na=False,
    dtype=str
)

# Find the exact Sky Lakes incident
mask = (
    (df["victim"] == "Sky Lakes Medical Center")
    & (df["incident-date"].str.startswith("2020-10-27"))
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 matching incident, found {mask.sum()}"
    )

# Verify the current status before updating
if df.loc[mask, "eligibility_status"].iloc[0] != "Pending review":
    raise ValueError(
        "Sky Lakes is not marked Pending review. "
        "Check the CSV before continuing."
    )

# Update the eligibility decision
df.loc[mask, "eligibility_status"] = "Eligible"

# No exclusion reason is needed
df.loc[mask, "exclusion_reason"] = ""

# Record supporting evidence
df.loc[mask, "review_notes"] = (
    "Sky Lakes Medical Center is a hospital that "
    "experienced a ransomware attack on October 27, 2020. "
    "The attack disrupted computer systems and hospital "
    "communications. Emergency and urgent care remained "
    "available. Duplicate check found one matching record."
)

df.loc[mask, "review_source"] = (
    "https://www.beckershospitalreview.com/cybersecurity/"
    "oregon-hospital-shuts-down-computer-system-after-"
    "ransomware-attack-4-notes.html"
)

# Confirm the total number of records
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

# Display the results
print("Sky Lakes Medical Center marked as Eligible.")
print("Total records:", len(df))
print(
    "Eligible records:",
    (df["eligibility_status"] == "Eligible").sum()
)
print(
    "Excluded records:",
    (df["eligibility_status"] == "Excluded").sum()
)
