import hashlib
import pandas as pd
from pathlib import Path

print("Final Project")


df = pd.read_csv("data/incidents.csv")

# important columns
important_columns = [
    "uuid",
    "victim",
    "sector",
    "incident-date",
    "attacker",
    "sources"
]

# Filter incidents
healthcare_df = df[
    df["sector"].fillna("").astype(str).str.strip().str.casefold()
    == "healthcare"
]

# first five incidents
print(healthcare_df[important_columns].head())

# Count incidents
print("Total healthcare incidents:", len(healthcare_df))


# Convert incident dates into date
healthcare_df = healthcare_df.copy()
healthcare_df["incident-date"] = pd.to_datetime(
    healthcare_df["incident-date"],
    errors="coerce"
)

# Filter incidents from 2020 - 2023
filtered_df = healthcare_df[
    healthcare_df["incident-date"].dt.year.between(2020, 2023)
]

# total number of matching incidents
print("\nHealthcare incidents from 2020 to 2023:")
print("Total:", len(filtered_df))

# incidents for each year
print("\nIncidents by year:")
print(
    filtered_df["incident-date"]
    .dt.year
    .value_counts()
    .sort_index()
)


# hash of each incident UUID
filtered_df = filtered_df.copy()

filtered_df["uuid_hash"] = filtered_df["uuid"].astype(str).apply(
    lambda value: hashlib.sha256(value.encode("utf-8")).hexdigest()
)

# first five UUIDs and their hashes
print("\nUUID and SHA-256 hash examples:")
print(filtered_df[["uuid", "uuid_hash"]].head())


# Sort incidents by SHA-256 hash
sorted_df = filtered_df.sort_values(
    by="uuid_hash",
    ascending=True
)

# first 10 sorted incidents
print("\nFirst 10 incidents sorted by SHA-256 hash:")
print(
    sorted_df[
        ["uuid", "victim", "incident-date", "uuid_hash"]
    ].head(10).to_string(index=False)
)

# total number of incidents
print("\nTotal sorted incidents:", len(sorted_df))


# sort incidents by year
for year in range(2020, 2024):

    # Select incidents for the current year
    year_df = sorted_df[
        sorted_df["incident-date"].dt.year == year
    ]

    print(f"\n===== Healthcare Incidents: {year} =====")
    print(f"Total candidates: {len(year_df)}")

    # first 10 incidents by SHA-256 hash
    print(
        year_df[
            ["uuid", "victim", "incident-date", "uuid_hash"]
        ].head(10).to_string(index=False)
    )


# Calculate the SHA-256 hash of each incident UUID
filtered_df = filtered_df.copy()

filtered_df["uuid_hash"] = filtered_df["uuid"].astype(str).apply(
    lambda value: hashlib.sha256(value.encode("utf-8")).hexdigest()
)

# first five UUIDs and their hashes
print("\nUUID and SHA-256 hash examples:")
print(filtered_df[["uuid", "uuid_hash"]].head())


# Sort incidents by SHA-256 hash
sorted_df = filtered_df.sort_values(
    by="uuid_hash",
    ascending=True
)

# first 10 sorted incidents
print("\nFirst 10 incidents sorted by SHA-256 hash:")
print(
    sorted_df[
        ["uuid", "victim", "incident-date", "uuid_hash"]
    ].head(10).to_string(index=False)
)

# total number of incidents
print("\nTotal sorted incidents:", len(sorted_df))


# Organize incidents by year
for year in range(2020, 2024):

    # Select incidents for the current year
    year_df = sorted_df[
        sorted_df["incident-date"].dt.year == year
    ]

    print(f"\n===== Healthcare Incidents: {year} =====")
    print(f"Total candidates: {len(year_df)}")

    # first 10 incidents by SHA-256 hash
    print(
        year_df[
            ["uuid", "victim", "incident-date", "uuid_hash"]
        ].head(10).to_string(index=False)
    )


# Create a copy of the sorted healthcare incidents
export_df = sorted_df.copy()

# Add the incident year
export_df["year"] = export_df["incident-date"].dt.year

# Sort by year and SHA-256 hash
export_df = export_df.sort_values(
    by=["year", "uuid_hash"],
    ascending=[True, True]
)

export_df.to_csv(
    "results/healthcare_candidates_sorted.csv",
    index=False
)

print("\nSorted healthcare candidates saved successfully!")
print("Total exported records:", len(export_df))

review_df = export_df[
    ["year", "uuid", "victim", "incident-date",
     "attacker", "sources", "uuid_hash"]
].copy()

# Add columns for manual eligibility review
review_df["eligibility_status"] = "Pending review"
review_df["exclusion_reason"] = ""
review_df["review_notes"] = ""
review_df["review_source"] = ""

# Save the eligibility review sheet

# Protect the eligibility review sheet
review_file = Path("results/healthcare_eligibility_review.csv")

# Only create the file if it does not already exist
if not review_file.exists():
    review_df.to_csv(review_file, index=False)
    print("\nEligibility review sheet created successfully!")
else:
    print("\nEligibility review sheet already exists.")
    print("Existing review decisions have been preserved.")


print("\nEligibility review sheet created successfully!")
print("Total records for review:", len(review_df))

first_2020 = export_df[
    export_df["year"] == 2020
].head(1)

print("\n===== First 2020 Incident =====")

print(
    first_2020[
        ["uuid", "victim", "incident-date",
         "attacker", "sources", "uuid_hash"]
    ].to_string(index=False)
)

second_2020 = export_df[
    export_df["year"] == 2020
].iloc[1:2]

print("\n===== Second 2020 Incident =====")

print(
    second_2020[
        ["uuid", "victim", "incident-date",
         "attacker", "sources", "uuid_hash"]
    ].to_string(index=False)
)

third_2020 = export_df[
    export_df["year"] == 2020
].iloc[2:3]

print("\n===== Third 2020 Incident =====")

print(
    third_2020[
        ["uuid", "victim", "incident-date",
         "attacker", "sources", "uuid_hash"]
    ].to_string(index=False)
)

fourth_2020 = export_df[
    export_df["year"] == 2020
].iloc[3:4]

print("\n===== Fourth 2020 Incident =====")

print(
    fourth_2020[
        ["uuid", "victim", "incident-date",
         "attacker", "sources", "uuid_hash"]
    ].to_string(index=False)
)

matches = export_df[
    export_df["victim"].str.contains(
        "Sky Lakes", case=False, na=False
    )
]

print("\n===== Sky Lakes Duplicate Check =====")
print("Matching records:", len(matches))

print(
    matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

fifth_2020 = export_df[
    export_df["year"] == 2020
].iloc[4:5]

print("\n===== Fifth 2020 Incident =====")

print(
    fifth_2020[
        [
            "uuid",
            "victim",
            "incident-date",
            "attacker",
            "sources",
            "uuid_hash",
        ]
    ].to_string(index=False)
)

brookside_matches = export_df[
    export_df["victim"].str.contains(
        "Brookside", case=False, na=False
    )
]

print("\n===== Brookside Duplicate Check =====")

print("Matching records:", len(brookside_matches))

print(
    brookside_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

sixth_2020 = export_df[
    export_df["year"] == 2020
].iloc[5:6]

print("\n===== Sixth 2020 Incident =====")

print(
    sixth_2020[
        [
            "uuid",
            "victim",
            "incident-date",
            "attacker",
            "sources",
            "uuid_hash",
        ]
    ].to_string(index=False)
)

dickinson_matches = export_df[
    export_df["victim"].str.contains(
        r"Dickingson|Dickinson",
        case=False,
        na=False
    )
]

print("\n===== Dickinson Duplicate Check =====")
print("Matching records:", len(dickinson_matches))

print(
    dickinson_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Seventh SHA-256-Sorted 2020 Incident =====")

if len(candidates_2020) < 7:
    raise ValueError("Fewer than 7 candidates found for 2020.")

seventh_incident = candidates_2020.iloc[6]

print("Victim:", seventh_incident["victim"])
print("Incident date:", seventh_incident["incident-date"])
print("Attacker:", seventh_incident["attacker"])
print("UUID:", seventh_incident["uuid"])

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Eighth SHA-256-Sorted 2020 Incident =====")

if len(candidates_2020) < 8:
    raise ValueError("Fewer than 8 candidates found for 2020.")

eighth_incident = candidates_2020.iloc[7]

print("Victim:", eighth_incident["victim"])
print("Incident date:", eighth_incident["incident-date"])
print("Attacker:", eighth_incident["attacker"])
print("UUID:", eighth_incident["uuid"])

valley_matches = export_df[
    export_df["victim"].str.contains(
        r"Valley Health",
        case=False,
        na=False
    )
]

print("\n===== Valley Health Duplicate Check =====")
print("Matching records:", len(valley_matches))

print(
    valley_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Ninth SHA-256-Sorted 2020 Incident =====")

if len(candidates_2020) < 9:
    raise ValueError("Fewer than 9 candidates found for 2020.")

ninth_incident = candidates_2020.iloc[8]

print("Victim:", ninth_incident["victim"])
print("Incident date:", ninth_incident["incident-date"])
print("Attacker:", ninth_incident["attacker"])
print("UUID:", ninth_incident["uuid"])

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Tenth SHA-256-Sorted 2020 Incident =====")

if len(candidates_2020) < 10:
    raise ValueError("Fewer than 10 candidates found for 2020.")

tenth_incident = candidates_2020.iloc[9]

print("Victim:", tenth_incident["victim"])
print("Incident date:", tenth_incident["incident-date"])
print("Attacker:", tenth_incident["attacker"])
print("UUID:", tenth_incident["uuid"])

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Eleventh SHA-256-Sorted 2020 Incident =====")

eleventh_incident = candidates_2020.iloc[10]

print("Victim:", eleventh_incident["victim"])
print("Incident date:", eleventh_incident["incident-date"])
print("Attacker:", eleventh_incident["attacker"])
print("UUID:", eleventh_incident["uuid"])
print("Sources:", eleventh_incident["sources"])

samaritan_matches = export_df[
    export_df["victim"].str.contains(
        "Samaritan",
        case=False,
        na=False
    )
]

print("\n===== Samaritan Health Duplicate Check =====")
print("Matching records:", len(samaritan_matches))

print(
    samaritan_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

candidates_2020 = export_df[
    export_df["year"].astype(str) == "2020"
].sort_values("uuid_hash").reset_index(drop=True)

print("\n===== Twelfth SHA-256-Sorted 2020 Incident =====")

twelfth_incident = candidates_2020.iloc[11]

print("Victim:", twelfth_incident["victim"])
print("Incident date:", twelfth_incident["incident-date"])
print("Attacker:", twelfth_incident["attacker"])
print("UUID:", twelfth_incident["uuid"])
print("Sources:", twelfth_incident["sources"])

alamance_matches = export_df[
    export_df["victim"].str.contains(
        "Alamance Skin",
        case=False,
        na=False
    )
]

print("\n===== Alamance Skin Center Duplicate Check =====")
print("Matching records:", len(alamance_matches))

print(
    alamance_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)

thirteenth_incident = candidates_2020.iloc[12]

print("\n===== Thirteenth SHA-256-Sorted 2020 Incident =====")
print("Victim:", thirteenth_incident["victim"])
print("Incident date:", thirteenth_incident["incident-date"])
print("Attacker:", thirteenth_incident["attacker"])
print("UUID:", thirteenth_incident["uuid"])
print("Sources:", thirteenth_incident["sources"])

dyras_matches = export_df[
    export_df["victim"].str.contains(
        "Dyras Dental",
        case=False,
        na=False
    )
]

print("\n===== Dyras Dental Duplicate Check =====")
print("Matching records:", len(dyras_matches))

print(
    dyras_matches[
        ["year", "uuid", "victim", "incident-date"]
    ].to_string(index=False)
)


