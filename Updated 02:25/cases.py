import pandas as pd

# Load your data from "cleaned_final_updated.csv" into a DataFrame
df = pd.read_csv("cleaned_patient_data.csv")
print(df.head())

# Define the 'data' dictionary representing binary bed type data with corrected names
data = {
    "Bed Type": ["Med/Surg", "ICU/Critical Care", "Psych", "Post_Acute_Care", "Burn", "Burn ICU", "Isolation", "Acute Rehabilitation Unit (ARU)"],
    "Georgetown": [1, 1, 1, 0, 0, 0, 0, 1],
    "GWU": [1, 1, 1, 1, 0, 0, 1, 1],
    "Howard": [1, 1, 1, 0, 0, 0, 1, 0],
    "NRH": [0, 0, 0, 0, 0, 0, 0, 1],
    "WHC": [1, 1, 1, 1, 1, 1, 1, 0],
    "Sibley": [1, 1, 1, 0, 0, 0, 1, 1],
    "Reston": [1, 1, 0, 0, 0, 0, 1, 1],
    "Fauquier": [1, 1, 0, 1, 0, 0, 1, 0],
    "FairOaks": [1, 1, 0, 1, 0, 0, 1, 0],
    "FFX": [1, 1, 1, 0, 0, 0, 1, 0],
    "Loudoun": [1, 1, 1, 1, 0, 0, 1, 0],
    "MaryWash": [1, 1, 1, 1, 0, 1, 0, 1],
    "MountVernon": [1, 1, 1, 1, 0, 0, 1, 1],
    "Novant": [1, 1, 1, 1, 0, 0, 0, 1],
    "Spotsylvania": [1, 1, 1, 1, 0, 0, 1, 0],
    "Stafford": [1, 1, 0, 1, 0, 0, 0, 0],
    "VHC": [1, 1, 1, 1, 0, 0, 1, 0]
}

# Extract the relevant case with a specific ID for demonstration (e.g., case ID 27)
case_id = 88
case_data = df[df['case_id'] == case_id]
# Create a list to store the bed types for the case
bed_types_for_case = []

# Define the bed type columns you want to check
bed_type_columns = ['first_bed_type', 'second_bed_type', 'third_bed_type', 'fourth_bed_type']

for bed_type in bed_type_columns:
    bed_type_value = case_data.iloc[0][bed_type]  # Get the value of the bed type for the case
    if pd.notna(bed_type_value):
        bed_types_for_case.append(bed_type_value)  # Append the bed type value to the list

matched_facilities = []


all_facilities = list(data.keys())[1:]  # Exclude "Bed Type" from keys to get facility names

for facility in all_facilities:
    facility_suitable = True
    for bed_type in bed_types_for_case:
        if bed_type in data['Bed Type']:
            bed_index = data['Bed Type'].index(bed_type)
            if data[facility][bed_index] == 0:  # Facility cannot accommodate this bed type
                facility_suitable = False
                break
    if facility_suitable:
        matched_facilities.append(facility)

# Populate the bed_types_for_case list with the bed types for the case


# Print the bed types for the case and the recommended facilities
print(f"Bed Types for Case {case_id}:", bed_types_for_case)
print("Recommended Facilities:", matched_facilities)
print("Severity:", case_data['arrival_severity'].iloc[0] )
