import pandas as pd

# Assuming the CSV file path and data dictionary are correctly set
csv_file_path = "cleaned_final_updated.csv"  # Correct path based on the initial script context

# Load your data from CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Data dictionary as provided
data = {
    "Bed Type": ["MedSurg", "ICU", "Psych", "Post_Acute_Care", "Burn", "BurnICU", "Isolation", "ARU"],
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

output_filename = "CaseDataWithRecommendations.xlsx"
writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')

for case_id in df['case_id'].unique():
    case_data = df[df['case_id'] == case_id]
    bed_types_for_case = []
    case_id_sheet_name = f"case{str(case_id).zfill(3)}"
    case_data.to_excel(writer, sheet_name=case_id_sheet_name, index=False)

    for column in ['first_bed_type', 'second_bed_type', 'third_bed_type', 'fourth_bed_type']:
        bed_type = case_data.iloc[0][column]
        if pd.notna(bed_type) and bed_type != "Post_Acute_Care":
            bed_type_corrected = bed_type.replace(" ", "").replace("BurnICU", "Burn ICU")
            bed_types_for_case.append(bed_type_corrected)

    all_facilities = list(data.keys())[1:]  # Exclude "Bed Type"
    for facility in all_facilities:
        if all(data[facility][data['Bed Type'].index(bt)] == 1 for bt in bed_types_for_case if bt in data['Bed Type']):
            facility_sheet_name = f"case{str(case_id).zfill(3)}_{facility}"
            pd.DataFrame({'Facility': [facility], 'Case ID': [case_id]}).to_excel(writer, sheet_name=facility_sheet_name, index=False)

writer._save()

print(f"Excel file with recommendations created and saved to {output_filename}")
