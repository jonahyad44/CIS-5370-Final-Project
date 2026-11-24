import pandas as pd
from pathlib import Path

file_path = Path("results/healthcare_eligibility_review.csv")

# Load the eligibility review CSV
df = pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact MultiCare incident
mask = (
    (df["victim"].str.strip() == "MultiCare")
    & (df["incident-date"].str.startswith("2020-12-02"))
    & (
        df["uuid"].str.strip()
        == "83929382-81b0-5145-be6a-3657a71457be"
    )
)

# Confirm exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 MultiCare record, found {mask.sum()}"
    )

# Check the current eligibility status
current_status = df.loc[
    mask, "eligibility_status"
].iloc[0]

if current_status not in ["", "Pending review"]:
    raise ValueError(
        f"Unexpected MultiCare status: {current_status}"
    )

# Mark MultiCare as Pending review
df.loc[mask, "eligibility_status"] = "Pending review"

# Leave exclusion reason blank
df.loc[mask, "exclusion_reason"] = ""

# Document the eligibility evidence
df.loc[mask, "review_notes"] = (
    "MultiCare is a healthcare delivery organization. "
    "The December 2, 2020 ransomware incident involved "
    "third-party IT provider Netgain Technology and "
    "affected MultiCare-related information through "
    "Woodcreek Provider Services. Reporting indicates "
    "that Woodcreek's medical records system was "
    "untouched, while information on an archive server "
    "was stolen. A direct ransomware attack on "
    "MultiCare's systems was not established. "
    "Pending clarification of third-party incident "
    "eligibility."
)

# Record the supporting source
df.loc[mask, "review_source"] = (
    "https://www.beckershospitalreview.com/cybersecurity/"
    "ransomware-attack-exposed-info-of-210k-multicare-"
    "patients-providers-workers.html"
)

# Confirm the expected number of records
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Check eligibility counts before saving
eligible_count = (
    df["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    df["eligibility_status"] == "Excluded"
).sum()

if eligible_count != 2 or excluded_count != 2:
    raise ValueError(
        f"Unexpected counts: {eligible_count} eligible, "
        f"{excluded_count} excluded. CSV not saved."
    )

# Save the updated CSV
df.to_csv(file_path, index=False)

# Display the results
print("MultiCare marked as Pending review.")
print("Total records:", len(df))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print(
    "MultiCare status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)
