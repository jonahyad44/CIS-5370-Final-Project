import pandas as pd
from pathlib import Path

backup_path = Path(
    "results/healthcare_eligibility_review_before_dickinson.csv"
)

updated_path = Path(
    "results/healthcare_eligibility_review.csv"
)

# Load the backup and updated CSV
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

# Confirm dimensions and columns
assert backup.shape == updated.shape, (
    "CSV dimensions changed."
)

assert backup.columns.tolist() == updated.columns.tolist(), (
    "CSV columns changed."
)

assert len(updated) == 670, (
    "Expected 670 records."
)

# Confirm UUIDs and row order are unchanged
assert backup["uuid"].tolist() == updated["uuid"].tolist(), (
    "UUIDs or row ordering changed."
)

# Find the exact Dickinson record
# The dataset uses the spelling "Dickingson"
mask = (
    (updated["victim"].str.strip()
     == "Dickingson County Healthcare System")
    & (updated["incident-date"].str.startswith("2020-10-17"))
)

assert mask.sum() == 1, (
    "Expected exactly one Dickinson record."
)

# Only these review fields may change
review_fields = [
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source",
]

# Confirm original dataset fields are unchanged
other_fields = [
    col for col in updated.columns
    if col not in review_fields
]

assert backup[other_fields].equals(
    updated[other_fields]
), "An original dataset field was changed."

# Confirm other incidents' review fields are unchanged
assert backup.loc[~mask, review_fields].equals(
    updated.loc[~mask, review_fields]
), "Another incident's review fields changed."

# Check Dickinson's eligibility
dickinson = updated.loc[mask].iloc[0]

assert dickinson["eligibility_status"] == "Eligible", (
    "Dickingson was not marked Eligible."
)

assert dickinson["exclusion_reason"] == "", (
    "Dickingson has an unexpected exclusion reason."
)

assert dickinson["review_notes"].strip(), (
    "Dickingson review notes are missing."
)

assert "uppermichiganssource.com" in dickinson["review_source"], (
    "Dickingson supporting source is missing."
)

# Check eligibility totals
eligible_count = (
    updated["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    updated["eligibility_status"] == "Excluded"
).sum()

assert eligible_count == 2, (
    f"Expected 2 eligible records, found {eligible_count}"
)

assert excluded_count == 2, (
    f"Expected 2 excluded records, found {excluded_count}"
)

# Verify Sky Lakes remains Eligible
sky_lakes = updated[
    (updated["victim"] == "Sky Lakes Medical Center")
    & (updated["incident-date"].str.startswith("2020-10-27"))
]

assert len(sky_lakes) == 1
assert sky_lakes.iloc[0]["eligibility_status"] == "Eligible"

# Verify earlier exclusions remain intact
for victim in [
    "Dr Reddy's Laboratories",
    "Saint Francis Healthcare System",
]:
    rows = updated[updated["victim"] == victim]

    assert (
        rows["eligibility_status"] == "Excluded"
    ).any(), f"Previous exclusion missing: {victim}"

# Verify Brookside remains Pending review
brookside = updated[
    (updated["victim"] == "Brookside Surgery Center")
    & (updated["incident-date"].str.startswith("2020-01-23"))
]

assert len(brookside) == 1
assert brookside.iloc[0]["eligibility_status"] == "Pending review"

print("===== Dickinson Verification =====")
print("Verification PASSED.")
print("Total records:", len(updated))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print("Dickingson status:", dickinson["eligibility_status"])
print("Only Dickingson County Healthcare System's review fields changed.")
print("Previous eligibility decisions were preserved.")
