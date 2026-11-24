
import pandas as pd
from pathlib import Path

# Files to compare
backup_path = Path(
    "results/healthcare_eligibility_review_before_sky_lakes.csv"
)
updated_path = Path(
    "results/healthcare_eligibility_review.csv"
)

# Read both CSV files
backup = pd.read_csv(
    backup_path, dtype=str, keep_default_na=False
)
updated = pd.read_csv(
    updated_path, dtype=str, keep_default_na=False
)

# Confirm the same rows and columns are present
assert backup.shape == updated.shape, (
    "The CSV dimensions changed."
)

assert backup.columns.tolist() == updated.columns.tolist(), (
    "The CSV columns changed."
)

assert len(updated) == 670, (
    "Expected 670 records."
)

# Check that row identifiers and ordering are unchanged
assert backup["uuid"].tolist() == updated["uuid"].tolist(), (
    "The UUIDs or row ordering changed."
)

# Identify the Sky Lakes record
mask = (
    (updated["victim"] == "Sky Lakes Medical Center")
    & (updated["incident-date"].str.startswith("2020-10-27"))
)

assert mask.sum() == 1, (
    "Expected exactly one Sky Lakes incident."
)

# These are the only fields allowed to change
review_fields = [
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source",
]

# Confirm all other columns remain unchanged
other_fields = [
    col for col in updated.columns
    if col not in review_fields
]

assert backup[other_fields].equals(updated[other_fields]), (
    "A non-review field was changed."
)

# Confirm other incidents' review fields are unchanged
assert backup.loc[~mask, review_fields].equals(
    updated.loc[~mask, review_fields]
), "Another incident's review fields were changed."

# Verify the Sky Lakes eligibility decision
assert updated.loc[mask, "eligibility_status"].iloc[0] == "Eligible", (
    "Sky Lakes was not marked Eligible."
)

assert updated.loc[mask, "exclusion_reason"].iloc[0] == "", (
    "Sky Lakes has an unexpected exclusion reason."
)

assert updated.loc[mask, "review_notes"].iloc[0].strip(), (
    "Sky Lakes review notes are missing."
)

assert updated.loc[mask, "review_source"].iloc[0].strip(), (
    "Sky Lakes review source is missing."
)

# Confirm the overall eligibility counts
assert (
    updated["eligibility_status"] == "Eligible"
).sum() == 1, "Expected 1 eligible record."

assert (
    updated["eligibility_status"] == "Excluded"
).sum() == 2, "Expected 2 excluded records."

# Confirm previous exclusions remain intact
for victim in [
    "Dr Reddy's Laboratories",
    "Saint Francis Healthcare System",
]:
    rows = updated[updated["victim"] == victim]

    assert (
        rows["eligibility_status"] == "Excluded"
    ).any(), f"Exclusion missing for {victim}"

print("===== Sky Lakes Verification =====")
print("Verification PASSED.")
print("Total records:", len(updated))
print("Eligible records: 1")
print("Excluded records: 2")
print("Only Sky Lakes Medical Center's review fields changed.")
print("Previous exclusions were preserved.")
