
import pandas as pd
from pathlib import Path

# Load the eligibility review CSV
file_path = Path("results/healthcare_eligibility_review.csv")

df = pd.read_csv(
    file_path,
    keep_default_na=False,
    dtype=str
)

# Find the exact Saint Francis incident
mask = (
    (df["victim"] == "Saint Francis Healthcare System")
    & (df["incident-date"].str.startswith("2020-11-04"))
)

# Make sure exactly one incident matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 matching incident, found {mask.sum()}"
    )

# Update the eligibility decision
df.loc[mask, "eligibility_status"] = "Excluded"

df.loc[mask, "exclusion_reason"] = (
    "Ransomware attack occurred in 2019, "
    "outside the required 2020-2023 period"
)

df.loc[mask, "review_notes"] = (
    "The dataset lists November 4, 2020, "
    "but the source discusses a proposed "
    "settlement related to a 2019 ransomware "
    "attack. No new 2020 attack was established."
)

df.loc[mask, "review_source"] = (
    "https://news.bloomberglaw.com/class-action/"
    "hospital-patients-seek-ransomware-attack-"
    "settlement-approval"
)

# Protect the total number of records
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

print("Saint Francis Healthcare System marked as Excluded.")
print("Total records:", len(df))
print(
    "Excluded records:",
    (df["eligibility_status"] == "Excluded").sum()
)
