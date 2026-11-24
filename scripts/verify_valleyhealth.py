import pandas as pd
from pathlib import Path

backup_path = Path(
    "results/healthcare_eligibility_review_before_valley_health.csv"
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

# Confirm dimensions and columns are unchanged
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

# Find the exact Valley Health System record
mask = (
    (updated["victim"].str.strip() == "Valley Health System")
    & (updated["incident-date"].str.startswith("2020-08-22"))
    & (
        updated["uuid"].str.strip()
        == "185e8dd6-991e-54bc-976b-51b38cdc95c6"
    )
)

assert mask.sum() == 1, (
    "Expected exactly one Valley Health System record."
)

# Only these review fields may change
review_fields = [
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source",
]

# Verify original dataset fields are unchanged
original_fields = [
    col for col in updated.columns
    if col not in review_fields
]

assert backup[original_fields].equals(
    updated[original_fields]
), "An original dataset field changed."

# Verify other incidents' review fields are unchanged
assert backup.loc[~mask, review_fields].equals(
    updated.loc[~mask, review_fields]
), "Another incident's review fields changed."

# Confirm Valley Health System's updated status
valley = updated.loc[mask].iloc[0]

assert valley["eligibility_status"] == "Eligible", (
    "Valley Health System was not marked Eligible."
)

assert valley["exclusion_reason"] == "", (
    "Valley Health System has an unexpected exclusion reason."
)

assert valley["review_notes"].strip(), (
    "Valley Health System review notes are missing."
)

assert "ransomware" in valley["review_notes"].lower(), (
    "Review notes do not mention ransomware."
)

assert "databreaches.net" in valley["review_source"], (
    "Supporting source is missing."
)

# Confirm expected eligibility counts
eligible_count = (
    updated["eligibility_status"] == "Eligible"
).sum()

excluded_count = (
    updated["eligibility_status"] == "Excluded"
).sum()

assert eligible_count == 3, (
    f"Expected 3 eligible records, found {eligible_count}"
)

assert excluded_count == 2, (
    f"Expected 2 excluded records, found {excluded_count}"
)

# Confirm earlier eligibility decisions remain intact
expected_statuses = {
    "Sky Lakes Medical Center": "Eligible",
    "Dickingson County Healthcare System": "Eligible",
    "MultiCare": "Pending review",
    "Brookside Surgery Center": "Pending review",
    "Dr Reddy's Laboratories": "Excluded",
    "Saint Francis Healthcare System": "Excluded",
}

for victim, expected_status in expected_statuses.items():
    rows = updated[updated["victim"] == victim]

    assert (
        rows["eligibility_status"] == expected_status
    ).any(), (
        f"Expected status not found for {victim}: "
        f"{expected_status}"
    )

# Confirm the separate 2023 Valley Health record is unchanged
valley_2023 = (
    (updated["victim"] == "Valley Health System")
    & (updated["incident-date"].str.startswith("2023-09-28"))
)

assert valley_2023.sum() == 1, (
    "Expected one separate 2023 Valley Health record."
)

assert backup.loc[valley_2023].equals(
    updated.loc[valley_2023]
), "The 2023 Valley Health record changed."

# Display the verification results
print("===== Valley Health Verification =====")
print("Verification PASSED.")
print("Total records:", len(updated))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print("Valley Health status:", valley["eligibility_status"])
print("Only the 2020 Valley Health System review fields changed.")
print("Previous eligibility decisions were preserved.")
print("The separate 2023 Valley Health record was unchanged.")
