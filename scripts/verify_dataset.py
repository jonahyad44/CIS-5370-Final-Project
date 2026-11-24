
import pandas as pd

# Load the original backup and updated review file
backup = pd.read_csv(
    "results/healthcare_eligibility_review_backup.csv",
    keep_default_na=False,
    dtype=str
)

updated = pd.read_csv(
    "results/healthcare_eligibility_review.csv",
    keep_default_na=False,
    dtype=str
)

# Compare the number of records
print("Backup records:", len(backup))
print("Updated records:", len(updated))

# Check that columns and row order are unchanged
assert backup.columns.tolist() == updated.columns.tolist()
assert backup["uuid"].tolist() == updated["uuid"].tolist()

# Identify all changed cells
changes = backup.ne(updated)

changed_rows = changes.any(axis=1)

print("Changed rows:", changed_rows.sum())

# Show which fields changed
for index in updated.index[changed_rows]:
    changed_columns = changes.columns[changes.loc[index]].tolist()
    print("Changed victim:", updated.loc[index, "victim"])
    print("Changed columns:", changed_columns)

# Verify the intended exclusion
target = (
    (updated["victim"] == "Dr Reddy's Laboratories")
    & updated["incident-date"].str.startswith("2020-10-21")
)

assert target.sum() == 1
assert updated.loc[target, "eligibility_status"].iloc[0] == "Excluded"

# Verify that no other row changed
assert changed_rows.sum() == 1
assert (changed_rows & target).sum() == 1

# Verify only review fields changed
allowed_columns = {
    "eligibility_status",
    "exclusion_reason",
    "review_notes",
    "review_source"
}

actual_columns = set(
    changes.columns[changes.loc[target].iloc[0]].tolist()
)

assert actual_columns.issubset(allowed_columns)

print("\nVerification passed!")
print("Only the intended incident's review fields changed.")
