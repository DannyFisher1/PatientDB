import pandas as pd

def get_info(df): 
    # Define the 'data' dictionary representing binary bed type data with corrected names
    bed_data = {
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
    specialty_data = {
    "specialties": [
        "Trauma Surgery", "Cardiothoracic Surgery", "Orthopedic Surgery", "Neurosurgery – Spinal and Brain",
        "Vascular Surgery", "Interventional radiology", "OMFS", "ENT", "Urology", "General Surgery",
        "Trauma Ophthalmology", "Plastic Reconstructive", "Psychiatry", "Internal Medicine (Hospitalist)",
        "Infectious disease", "Neurology", "Cardiology", "Nephrology", "Pulmonary",
        "Intensive Daily OT", "Intensive Daily PT", "Prosthetics", "Neuro Rehab",
        "Orthopedics Rehab", "Mental Health Services - Medical (Psychiatrist)", "Mental Health Services - Therapist",
        "Visiting Nurse", "Home Health Aid (ADL)", "Wound Services", "Dialysis services",
        "Infusion services", "Pain management services", "Surgical Center services", "Other Rehab"],
    "Sibley": [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    "NRH": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "Howard": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    "WHC": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    "Reston": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    "Georgetown": [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    "GWU": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    "FairOaks": [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
    "FFX": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    "Fauquier": [0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    "Loudoun": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    "MaryWash": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    "Mount Vernon": [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    "Novant": [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    "Spotsylvania": [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    "Stafford": [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1],
    "VHC": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1]
    }

    bed_type_columns = ['first_bed_type', 'second_bed_type', 'third_bed_type', 'fourth_bed_type']

    for case_id in df['case_id'].unique():
        case_data = df[df['case_id'] == case_id]
        bed_types_for_case = []

        for bed_type in bed_type_columns:
            if bed_type in case_data.columns:
                bed_type_value = case_data.iloc[0][bed_type]
                if pd.notna(bed_type_value):
                    bed_types_for_case.append(bed_type_value)

        matched_facilities = []
        all_facilities = list(bed_data.keys())[1:]  # Exclude "Bed Type" from keys to get facility names

        for facility in all_facilities:
            facility_suitable = True
            for bed_type in bed_types_for_case:
                if bed_type in bed_data['Bed Type']:
                    bed_index = bed_data['Bed Type'].index(bed_type)
                    if bed_data[facility][bed_index] == 0:
                        facility_suitable = False
                        break
            if facility_suitable:
                matched_facilities.append(facility)

        spec_columns=['first_bed_PRIMARY','second_bed_PRIMARY','third_bed_PRIMARY','fourth_bed_PRIMARY',]
        # Print the bed types for the case and the recommended facilities
        print(f"\nCase ID: {case_id}")
        print(f"Bed Types for Case: {bed_types_for_case}")
        print("Recommended Facilities:", matched_facilities)
        print("Severity:", case_data['arrival_severity'].iloc[0])
