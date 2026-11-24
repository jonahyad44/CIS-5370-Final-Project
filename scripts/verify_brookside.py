import pandas as pd
from pathlib import Path

backup_path = Path(
    "results/healthcare_eligibility_review_before_brookside.csv"
)

updated_path = Path(
    "results/healthcare_eligibility_review.csv"
)

# Load both CSV files
backup = pd.read_csv(
    backup_path,
    dtype=str,
    keep_default_na=False
)

updated = pd.read_csv(
    updated_path,
    dtype=str,
    keep_default_na=False
)

# Confirm record counts and columns
assert backup.shape == updated.shape, (
    "CSV dimensions changed."
)

assert backup.columns.tolist() == updated.columns.tolist(), (
    "CSV columns changed."
)

assert len(updated) == 670, (
    "Expected 670 records."
)

# Confirm UUIDs and row ordering are unchanged
assert backup["uuid"].tolist() == updated["uuid"].tolist(), (
    "UUIDs or row ordering changed."
)

# Find the exact Brookside incident
mask = (
    (updated["victim"] == "Brookside Surgery Center")
    & (updated["incident-date"].str.startswith("2020-01-23"))
)

assert mask.sum() == 1, (
    "Expected exactly one Brookside incident."
)

# Only these review fields may change
review_fields = [
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source",
]

# Check all original dataset fields
other_fields = [
    col for col in updated.columns
    if col not in review_fields
]

assert backup[other_fields].equals(
    updated[other_fields]
), "An original dataset field was changed."

# Check all other incidents' review fields
assert backup.loc[~mask, review_fields].equals(
    updated.loc[~mask, review_fields]
), "Another incident's review fields changed."

# Verify Brookside's status and documentation
brookside = updated.loc[mask].iloc[0]

assert brookside["eligibility_status"] == "Pending review", (
    "Brookside status is incorrect."
)

assert brookside["exclusion_reason"] == "", (
    "Brookside has an unexpected exclusion reason."
)

assert "actual attack date" in brookside["review_notes"].lower(), (
    "Brookside's date uncertainty was not documented."
)

assert "detroit.cbslocal.com" in brookside["review_source"], (
    "Brookside's supporting source is missing."
)

# Verify overall counts
eligible_count = (
    updated["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    updated["eligibility_status"] == "Excluded"
).sum()

assert eligible_count == 1, (
    f"Expected 1 eligible record, found {eligible_count}"
)

assert excluded_count == 2, (
    f"Expected 2 excluded records, found {excluded_count}"
)

# Verify previous decisions
sky_lakes = updated[
    (updated["victim"] == "Sky Lakes Medical Center")
    & (updated["incident-date"].str.startswith("2020-10-27"))
]

assert len(sky_lakes) == 1
assert sky_lakes.iloc[0]["eligibility_status"] == "Eligible"

for victim in [
    "Dr Reddy's Laboratories",
    "Saint Francis Healthcare System",
]:
    rows = updated[updated["victim"] == victim]

    assert (
        rows["eligibility_status"] == "Excluded"
    ).any(), f"Previous exclusion missing: {victim}"

print("===== Brookside Verification =====")
print("Verification PASSED.")
print("Total records:", len(updated))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print("Brookside status:", brookside["eligibility_status"])
print("Only Brookside Surgery Center's review fields changed.")
print("Previous eligibility decisions were preserved.")