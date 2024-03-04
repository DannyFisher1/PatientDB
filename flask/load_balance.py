import logging

data = {
        "Bed Type": ["Med/Surg", "ICU/Critical Care", "Psych", "Post_Acute_Care", "Burn", "Burn ICU", "Isolation", "Acute Rehabilitation Unit (ARU)"],
        "Georgetown": [24, 6, 1, 0, 0, 0, 0, 4],
        "GWU": [23, 6, 2, 2, 0, 0, 1, 2],
        "Howard": [27, 2, 2, 0, 0, 0, 1, 0],
        "NRH": [0, 0, 0, 0, 0, 0, 0, 14],
        "WHC": [57, 11, 3, 1, 2, 2, 2, 0],
        "Sibley": [17, 2, 1, 0, 0, 0, 2, 1],
        "Reston": [14, 2, 0, 0, 0, 0, 1, 3],
        "Fauquier": [6, 2, 0, 1, 0, 0, 1, 0],
        "FairOaks": [10, 1, 0, 3, 0, 0, 1, 0],
        "FFX": [53, 10, 4, 0, 0, 0, 11, 0],
        "Loudoun": [12, 1, 2, 3, 0, 0, 1, 0],
        "MaryWash": [27, 4, 7, 2, 0, 0, 0, 1],
        "Mount Vernon": [10, 3, 3, 5, 0, 0, 1, 2],
        "Novant": [6, 1, 3, 2, 0, 0, 0, 2],
        "Spotsylvania": [4, 2, 3, 2, 0, 0, 1, 0],
        "Stafford": [3, 1, 0, 3, 0, 0, 0, 0],
        "VHC": [18, 3, 4, 2, 0, 0, 2, 2]
    }

def update_bed_count_for_case(case_result, bed_counts):
    if case_result["Assigned"]:
        facility = case_result["Facility"]
        needed_bed_types = case_result["Bed Typed Needed"]
        
        for bed_type in needed_bed_types:
            if bed_counts.at[bed_type, facility] > 0:
                bed_counts.at[bed_type, facility] -= 1
            else:
                logging.warning(f"Attempted to assign a bed of type '{bed_type}' at '{facility}', but none were available.")
    
    return bed_counts
