import pandas as pd
import logging

def match_bed(df):
    bed_type_replacements = {
        "Long-term Care Facility": "Post_Acute_Care",
        "Medical Hotel/Equivalent": "Post_Acute_Care",
        "medical Hotel/Equivalent": "Post_Acute_Care",
        "Skilled Nursing Facility (SNF)": "Post_Acute_Care",
        "skilled nursing facility (snf)": "Post_Acute_Care",
        "Rehabilitation Hospital": "Acute Rehabilitation Unit (ARU)",
        "burn icu": "Burn ICU",
        "burn": "Burn",
        "acute rehabilitation unit (aru)": "Acute Rehabilitation Unit (ARU)",
        "icu/critical care": "ICU/Critical Care",
        "med/surg": "Med/Surg",
        "rehabilitation hospital": "Acute Rehabilitation Unit (ARU)",
        "long-term care facility": "Post_Acute_Care"
    }

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
        "MaryWash": [1, 1, 1, 1, 0, 0, 0, 1],
        "MountVernon": [1, 1, 1, 1, 0, 0, 1, 1],
        "Novant": [1, 1, 1, 1, 0, 0, 0, 1],
        "Spotsylvania": [1, 1, 1, 1, 0, 0, 1, 0],
        "Stafford": [1, 1, 0, 1, 0, 0, 0, 0],
        "VHC": [1, 1, 1, 1, 0, 0, 1, 0]
    }

    bed_type_columns = ['first_bed_type', 'second_bed_type', 'third_bed_type', 'fourth_bed_type']

    for column in bed_type_columns:
        if column in df.columns:
            df[column] = df[column].map(bed_type_replacements).fillna(df[column])

    results = []

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
        
        # Append results for this case to the list
        results.append({
            "Case ID": case_id,
            "Bed Types Needed": bed_types_for_case,
            "Recommended Facilities bed": matched_facilities,
            "Severity": case_data['arrival_severity'].iloc[0]
        })
        
    return results


def match_spec(df):
    spec_data = {
    "spec": [
        "Trauma Surgery", "Cardiothoracic Surgery", "Orthopedic Surgery", "Neurosurgery – Spinal and Brain",
        "Vascular Surgery", "Interventional radiology", "OMFS", "ENT", "Urology", "General Surgery",
        "Trauma Ophthalmology", "Plastic Reconstructive", "Psychiatry", "Internal Medicine (Hospitalist)",
        "Infectious disease", "Neurology", "Cardiology", "Nephrology", "Pulmonary",
        "Intensive Daily OT", "Intensive Daily PT", "Prosthetics", "Neuro Rehab",
        "Orthopedics Rehab", "Mental Health Services - Medical (Psychiatrist)", "Mental Health Services - Therapist",
        "Visiting Nurse", "Home Health Aid (ADL)", "Wound Services", "Dialysis services",
        "Infusion services", "Pain management services", "Surgical Center services", "Other Rehab",],
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

    spec_type_columns=['first_bed_PRIMARY','first_bed_SECONDARY', 'first_bed_TERTIARY', 'second_bed_PRIMARY','third_bed_PRIMARY','second_bed_PRIMARY', 'second_bed_SECONDARY', 'second_bed_TERTIARY', 'third_bed_PRIMARY', 'third_bed_SECONDARY', 'third_bed_TERTIARY']
    
    results = []

    for case_id in df['case_id'].unique():
        case_data = df[df['case_id'] == case_id]
        spec_types_for_case = []

        for spec_type in spec_type_columns:
            if spec_type in case_data.columns:
                spec_type_value = case_data.iloc[0][spec_type]
                if pd.notna(spec_type_value) and spec_type_value not in spec_types_for_case:
                    spec_types_for_case.append(spec_type_value)

        spec_types_for_case = list(set(spec_types_for_case))  # Ensure uniqueness

        matched_facilities = []
        all_facilities = list(spec_data.keys())[1:]  # Exclude "spec" from keys to get facility names

        for facility in all_facilities:
            facility_suitable = True
            for spec_type in spec_types_for_case:
                if spec_type in spec_data['spec']:
                    spec_index = spec_data['spec'].index(spec_type)
                    if spec_data[facility][spec_index] == 0:
                        facility_suitable = False
                        break
            if facility_suitable:
                matched_facilities.append(facility)

        # Append results for this case to the list
        results.append({
            "Case ID": case_id,
            "Spec Types Needed": spec_types_for_case,
            "Recommended Facilities spec": matched_facilities,
            "Severity": case_data['arrival_severity'].iloc[0]
        })

    return results

def get_info(df):
    beds = match_bed(df)
    specs = match_spec(df)
    common_results = []
    
    for bed in beds:
        for spec in specs:
            if bed['Case ID'] == spec['Case ID']:
                # Intersection of recommended facilities
                common_facilities = list(set(bed['Recommended Facilities bed']) & set(spec['Recommended Facilities spec']))
                common_results.append({
                    "Case ID": bed['Case ID'],
                    "Severity": bed['Severity'],
                    "Bed Typed Needed": bed['Bed Types Needed'],
                    "Specialties Needed": spec['Spec Types Needed'],
                    "Common Recommended Facilities": common_facilities,
                        
                })
    for result in common_results:
        if 'Severity' in result:
            result['Severity'] = str(result['Severity']).upper()

    severity_order = {"CRITICAL": 1, "SEVERE": 2, "MODERATE": 3, "SERIOUS": 4, "MINOR":5,  "MILD": 6}
    common_results.sort(key=lambda x: severity_order.get(x['Severity'], 7))

    
    # Logging
    if not common_results:
        logging.warning("No matching facilities found.")
    elif not common_results[0]['Common Recommended Facilities']:
        logging.warning("No common recommended facilities found for the given cases.")
    
    return common_results
