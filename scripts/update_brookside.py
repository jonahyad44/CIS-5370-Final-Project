import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact Brookside incident
mask = (
    (df["victim"] == "Brookside Surgery Center")
    & (df["incident-date"].str.startswith("2020-01-23"))
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 Brookside record, found {mask.sum()}"
    )

# Check that the current status has not been finalized
current_status = df.loc[mask, "eligibility_status"].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected Brookside status: {current_status}"
    )

# Document the review decision
df.loc[mask, "eligibility_status"] = "Pending review"

# Brookside is not excluded
df.loc[mask, "exclusion_reason"] = ""

# Record findings and remaining uncertainty
df.loc[mask, "review_notes"] = (
    "Brookside Surgery Center is an outpatient healthcare "
    "facility in Battle Creek, Michigan. An archived CBS "
    "Detroit article published January 23, 2020 confirms "
    "a ransomware attack affecting the center's computers "
    "and reports a $6,500 ransom demand and patient data "
    "deletion. The actual attack date is not stated. "
    "The publication date must not be treated as the "
    "confirmed attack date. One Brookside-named record "
    "was found in the filtered dataset. Pending independent "
    "confirmation that the attack occurred in 2020."
)

# Preserve the original supporting source
df.loc[mask, "review_source"] = (
    "https://detroit.cbslocal.com/2020/01/23/"
    "battle-creek-medical-center-data-hacked-and-held-for-ransom/"
)

# Check total records before saving
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Save the updated review CSV
df.to_csv(file_path, index=False)

# Display results
print("Brookside Surgery Center documented as Pending review.")
print("Total records:", len(df))
print(
    "Eligible records:",
    (df["eligibility_status"] == "Eligible").sum()
)
print(
    "Excluded records:",
    (df["eligibility_status"] == "Excluded").sum()
)
print(
    "Brookside status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)