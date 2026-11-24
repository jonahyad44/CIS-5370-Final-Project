import pandas as pd

# Load the eligibility review CSV
csv_path = "results/healthcare_eligibility_review.csv"

df = pd.read_csv(
    csv_path,
    dtype=str,
    keep_default_na=False
)

# Find the exact Dyras Dental record
mask = (
    (df["victim"] == "Dyras Dental")
    & (df["incident-date"].str.startswith("2020-12-04"))
    & (
        df["uuid"]
        == "6715daa3-0ee2-5652-a4b4-a982cfdb966a"
    )
)

# Safety checks
assert len(df) == 670, "Unexpected total record count."
assert mask.sum() == 1, "Expected exactly one Dyras Dental record."

# Mark Dyras Dental as Eligible
df.loc[mask, "eligibility_status"] = "Eligible"
df.loc[mask, "exclusion_reason"] = ""

# Document the evidence and limitations
df.loc[mask, "review_notes"] = (
    "Dental healthcare provider affected by Egregor ransomware. "
    "Patient and employee information was reportedly leaked. "
    "A March 2021 update reported approximately 2,745 affected patients. "
    "Direct patient-care disruption was not confirmed. "
    "The dataset lists December 4, 2020; exact attack date "
    "was not independently confirmed."
)

# Record the source
df.loc[mask, "review_source"] = (
    "https://databreaches.net/2020/12/04/"
    "update-on-dyras-dental-ransomware-attack/"
)

# Save the updated CSV
df.to_csv(csv_path, index=False)

# Display results
print("Dyras Dental marked as Eligible.")
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
    "Dyras Dental status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)
