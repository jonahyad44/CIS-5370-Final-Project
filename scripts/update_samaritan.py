import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact Samaritan Health record
mask = (
    (df["victim"].str.strip() == "Samaritan Health")
    & (df["incident-date"].str.strip() == "2020-07-25")
    & (
        df["uuid"].str.strip()
        == "5ab5149c-c9d0-5962-87cf-2b5f3a374e42"
    )
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 Samaritan Health record, found {mask.sum()}"
    )

# Protect previous eligibility decisions
current_status = df.loc[
    mask, "eligibility_status"
].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected current status: {current_status}"
    )

# Mark Samaritan Health Eligible
df.loc[mask, "eligibility_status"] = "Eligible"

df.loc[mask, "exclusion_reason"] = ""

# Record the supporting evidence
df.loc[mask, "review_notes"] = (
    "Samaritan Health is a healthcare delivery organization "
    "in Watertown, New York. A ransomware attack on "
    "July 25, 2020 disrupted hospital computer systems "
    "and affected clinical operations. Some clinics "
    "continued providing care while computer systems "
    "were unavailable. Recovery continued for several "
    "weeks. A duplicate check found no matching "
    "record of the same incident."
)

# Record the original supporting source
df.loc[mask, "review_source"] = (
    "https://www.beckershospitalreview.com/cybersecurity/"
    "new-york-health-system-clinics-still-offline-after-"
    "july-ransomware-attack-4-details.html"
)

# Confirm dataset size
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Confirm expected counts before saving
eligible_count = (
    df["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    df["eligibility_status"] == "Excluded"
).sum()

if eligible_count != 4 or excluded_count != 2:
    raise ValueError(
        f"Unexpected counts: {eligible_count} eligible, "
        f"{excluded_count} excluded. CSV not saved."
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

# Display results
print("Samaritan Health marked as Eligible.")
print("Total records:", len(df))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print(
    "Samaritan Health status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)