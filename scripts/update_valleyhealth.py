import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

# Load the eligibility review CSV
df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact 2020 Valley Health System incident
mask = (
    (df["victim"].str.strip() == "Valley Health System")
    & (df["incident-date"].str.startswith("2020-08-22"))
    & (
        df["uuid"].str.strip()
        == "185e8dd6-991e-54bc-976b-51b38cdc95c6"
    )
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 Valley Health record, found {mask.sum()}"
    )

# Check the current eligibility status
current_status = df.loc[
    mask, "eligibility_status"
].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected Valley Health status: {current_status}"
    )

# Mark the incident Eligible
df.loc[mask, "eligibility_status"] = "Eligible"

# No exclusion reason is needed
df.loc[mask, "exclusion_reason"] = ""

# Document the supporting evidence
df.loc[mask, "review_notes"] = (
    "Valley Health Systems is a healthcare delivery "
    "organization operating facilities in West Virginia, "
    "Ohio, and Kentucky. Public reporting confirms a "
    "ransomware attack discovered on August 22, 2020. "
    "The attack disrupted access to some computer systems. "
    "Patient care continued using emergency procedures. "
    "REvil/Sodinokibi reportedly claimed responsibility. "
    "The 2020 incident was checked for duplicates; "
    "other Valley Health-named records have different "
    "organizations or incident dates."
)

# Record the supporting source
df.loc[mask, "review_source"] = (
    "https://databreaches.net/2020/08/28/"
    "valley-health-system-recovering-from-ransomware-"
    "attack-while-maintaining-patient-care/"
)

# Confirm the total number of records before saving
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Check expected eligibility counts before saving
eligible_count = (
    df["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    df["eligibility_status"] == "Excluded"
).sum()

if eligible_count != 3 or excluded_count != 2:
    raise ValueError(
        f"Unexpected counts: {eligible_count} eligible, "
        f"{excluded_count} excluded. CSV not saved."
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

# Display the results
print("Valley Health System marked as Eligible.")
print("Total records:", len(df))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print(
    "Valley Health status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)

