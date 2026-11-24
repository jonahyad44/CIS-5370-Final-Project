
import pandas as pd

# Load the backup and updated CSV
backup = pd.read_csv(
    "results/healthcare_eligibility_review_before_saint_francis.csv",
    dtype=str,
    keep_default_na=False
)

updated = pd.read_csv(
    "results/healthcare_eligibility_review.csv",
    dtype=str,
    keep_default_na=False
)

# Check record count and row order
assert len(backup) == len(updated) == 670
assert backup.columns.tolist() == updated.columns.tolist()
assert backup["uuid"].tolist() == updated["uuid"].tolist()

print("Backup records:", len(backup))
print("Updated records:", len(updated))

# Find differences between the two files
changes = backup.ne(updated)
changed_rows = changes.any(axis=1)

print("Changed rows:", changed_rows.sum())

# Find the Saint Francis incident
target = (
    (updated["victim"] == "Saint Francis Healthcare System")
    & (updated["incident-date"] == "2020-11-04")
)

assert target.sum() == 1

# Verify only the intended incident changed
assert changed_rows.sum() == 1
assert (changed_rows & target).sum() == 1

# Identify the changed columns
changed_columns = changes.columns[
    changes.loc[target].iloc[0]
].tolist()

print("Changed victim:", updated.loc[target, "victim"].iloc[0])
print("Changed columns:", changed_columns)

# Verify only review fields changed
expected_columns = {
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source"
}

assert set(changed_columns) == expected_columns

# Verify both exclusion decisions
assert updated.loc[
    target, "eligibility_status"
].iloc[0] == "Excluded"

dr_reddys = updated["victim"] == "Dr Reddy's Laboratories"

assert dr_reddys.sum() == 1
assert updated.loc[
    dr_reddys, "eligibility_status"
].iloc[0] == "Excluded"

assert (updated["eligibility_status"] == "Excluded").sum() == 2

print("\nVerification passed!")
print("Only Saint Francis Healthcare System's review fields changed.")
print("Both previous exclusion decisions are preserved.")
