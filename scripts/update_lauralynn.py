import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact LauraLynn record
mask = (
    (df["victim"].str.strip() == "Laura Lynn")
    & (df["incident-date"].str.strip() == "2020-08-01")
    & (
        df["uuid"].str.strip()
        == "a5717644-e55f-5427-a841-15248af60295"
    )
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 LauraLynn record, found {mask.sum()}"
    )

# Protect existing decisions
current_status = df.loc[
    mask, "eligibility_status"
].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected current status: {current_status}"
    )

# Update eligibility fields
df.loc[mask, "eligibility_status"] = "Pending review"

df.loc[mask, "exclusion_reason"] = (
    "Third-party ransomware involvement; direct attack "
    "on LauraLynn systems not established."
)

df.loc[mask, "review_notes"] = (
    "LauraLynn Children's Hospice is a healthcare delivery "
    "organization in Ireland. Its 2020 incident relates to "
    "a ransomware attack against Blackbaud, a third-party "
    "software provider. LauraLynn supporter information "
    "was affected, but available evidence does not "
    "establish a direct ransomware attack on LauraLynn's "
    "own systems. The dataset's August 1, 2020 incident "
    "date is not independently confirmed. One matching "
    "LauraLynn record was found in the dataset. "
    "Pending review of third-party-only eligibility."
)

df.loc[mask, "review_source"] = (
    "https://www.businesspost.ie/business/"
    "irish-charities-hit-in-global-ransomware-hack-"
    "attack-0f4bcd15; "
    "https://www.lauralynn.ie/news/"
    "lauralynn-statement-on-blackbaud-breach"
)

# Confirm dataset size
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Confirm eligibility counts
eligible_count = (
    df["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    df["eligibility_status"] == "Excluded"
).sum()

pending_count = (
    df["eligibility_status"] == "Pending review"
).sum()

if eligible_count != 3 or excluded_count != 2:
    raise ValueError(
        "Unexpected eligibility counts. CSV not saved."
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

print("LauraLynn marked as Pending review.")
print("Total records:", len(df))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print("Pending review records:", pending_count)
print(
    "LauraLynn status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)