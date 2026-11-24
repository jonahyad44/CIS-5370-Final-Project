import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

# Load the eligibility review CSV
df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact incident
# Preserve the original dataset spelling: Dickingson
mask = (
    (df["victim"].str.strip() == "Dickingson County Healthcare System")
    & (df["incident-date"].str.startswith("2020-10-17"))
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 Dickingson record, found {mask.sum()}"
    )

# Check the current eligibility status
current_status = df.loc[mask, "eligibility_status"].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected Dickingson status: {current_status}"
    )

# Mark the incident Eligible
df.loc[mask, "eligibility_status"] = "Eligible"

# No exclusion reason is needed
df.loc[mask, "exclusion_reason"] = ""

# Record the supporting evidence
df.loc[mask, "review_notes"] = (
    "Dickingson County Healthcare System is a healthcare "
    "delivery organization operating a hospital and clinics. "
    "Public reporting confirms a ransomware attack discovered "
    "on October 17, 2020. The incident disrupted computer "
    "systems, and staff used manual procedures while patient "
    "services continued. One matching record was found in "
    "the filtered dataset. The original dataset spells the "
    "organization name as Dickingson."
)

# Record the supporting source
df.loc[mask, "review_source"] = (
    "https://www.uppermichiganssource.com/2020/10/20/"
    "dickinson-county-healthcare-system-responding-to-malware-attack/"
)

# Confirm the total number of records before saving
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Confirm the expected eligibility counts
eligible_count = (df["eligibility_status"] == "Eligible").sum()
excluded_count = (df["eligibility_status"] == "Excluded").sum()

if eligible_count != 2 or excluded_count != 2:
    raise ValueError(
        f"Unexpected counts: {eligible_count} eligible, "
        f"{excluded_count} excluded. CSV not saved."
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

# Display the results
print("Dickingson County Healthcare System marked as Eligible.")
print("Total records:", len(df))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print(
    "Dickingson status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)