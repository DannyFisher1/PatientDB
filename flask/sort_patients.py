import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_crit_facilities(cases):
    # Initial bed count data
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

    bed_counts = pd.DataFrame(data).set_index('Bed Type')

    critical_cases = [case for case in cases if case['Severity'] == 'CRITICAL']
    logging.info(f'Amount of Critical Cases: {len(critical_cases)}')

    case_outcomes = []  # Stores outcomes for each case

    for case in critical_cases:
        case_result = {
            "Case ID": case['Case ID'], 
            "Assigned": False, 
            "Facility": None, 
            "Reason": None
        }
        needed_bed_types = case['Bed Typed Needed']
        recommended_facilities = case['Common Recommended Facilities']
        
        for facility in recommended_facilities:
            if all(bed_counts.loc[bed_type, facility] > 0 for bed_type in needed_bed_types):
                case_result["Assigned"] = True
                case_result["Facility"] = facility
                for bed_type in needed_bed_types:
                    bed_counts.at[bed_type, facility] -= 1  # Update bed counts
                logging.info(f"Case ID {case['Case ID']} assigned to {facility}")
                break

        if not case_result["Assigned"]:
            case_result["Reason"] = "No facility has all needed bed types available."
            logging.warning(
                f"Case ID {case['Case ID']} could not be assigned to any facility. "
                "Reason: {case_result['Reason']}"
            )

        case_outcomes.append(case_result)

    logging.info(
        "Unassigned Cases: " + 
        ", ".join([str(cid["Case ID"]) for cid in case_outcomes if not cid["Assigned"]])
    )
    logging.info(f"\nUpdated Bed Counts:\n{bed_counts}")

    return case_outcomes, bed_counts