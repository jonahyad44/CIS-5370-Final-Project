import pandas as pd
from pathlib import Path

backup_path = Path(
    "results/healthcare_eligibility_review_before_multicare.csv"
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

# Confirm the dataset dimensions and columns
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

# Find the exact MultiCare record
mask = (
    (updated["victim"].str.strip() == "MultiCare")
    & (updated["incident-date"].str.startswith("2020-12-02"))
    & (
        updated["uuid"].str.strip()
        == "83929382-81b0-5145-be6a-3657a71457be"
    )
)

assert mask.sum() == 1, (
    "Expected exactly one MultiCare record."
)

# Only these review fields are allowed to change
review_fields = [
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source",
]

# Verify all original dataset fields are unchanged
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

# Check MultiCare's updated review fields
multicare = updated.loc[mask].iloc[0]

assert multicare["eligibility_status"] == "Pending review", (
    "MultiCare was not marked Pending review."
)

assert multicare["exclusion_reason"] == "", (
    "MultiCare has an unexpected exclusion reason."
)

assert multicare["review_notes"].strip(), (
    "MultiCare review notes are missing."
)

assert "Netgain Technology" in multicare["review_notes"], (
    "MultiCare review notes do not mention Netgain."
)

assert "beckershospitalreview.com" in multicare["review_source"], (
    "MultiCare supporting source is missing."
)

# Check the eligibility counts
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

# Confirm earlier decisions remain intact
expected_statuses = {
    "Sky Lakes Medical Center": "Eligible",
    "Dickingson County Healthcare System": "Eligible",
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

# Print the results
print("===== MultiCare Verification =====")
print("Verification PASSED.")
print("Total records:", len(updated))
print("Eligible records:", eligible_count)
print("Excluded records:", excluded_count)
print("MultiCare status:", multicare["eligibility_status"])
print("Only MultiCare's review fields changed.")
print("Previous eligibility decisions were preserved.")
