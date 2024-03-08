import random
import pandas as pd
import logging
import load_balance as lb

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_crit_facilities(cases):
    bed_counts = pd.DataFrame(lb.data).set_index('Bed Type')

    selected_traffic_condition = random.choice(['Low', 'Medium', 'High'])
    logging.info(f"Selected traffic condition for all cases: {selected_traffic_condition}")

    critical_cases = [case for case in cases if case['Severity'] == 'CRITICAL']
    logging.info(f'Amount of Critical Cases: {len(critical_cases)}')

    case_outcomes = []
    recs = []
    for case in critical_cases:
        case_result = {
            "Case ID": case['Case ID'],
            "Assigned": False,
            "Facility": None,
            "Reason": None,
            "Travel Time": None,
            "Bed Typed Needed": case['Bed Typed Needed']  # Assume this information is provided for each case
        }

        recommended_facilities = case['Common Recommended Facilities']
        sorted_facilities = sorted(recommended_facilities, key=lambda x: transportation_times[x][selected_traffic_condition])
        facilities_times = [(facility, transportation_times[facility][selected_traffic_condition]) for facility in sorted_facilities]
        recs1 = {
            "Case ID": case['Case ID'],
            "Facility": dict(facilities_times),
            'Specialties Needed': case['Specialties Needed'],
            "Bed Types Needed": case['Bed Typed Needed']  # Assume this information is provided for each case
        }
        recs.append(recs1)
        print(recs)
        for facility in sorted_facilities:
            needed_bed_types = case['Bed Typed Needed']
            if all(bed_counts.loc[bed_type, facility] > 0 for bed_type in needed_bed_types):
                case_result["Assigned"] = True
                case_result["Facility"] = facility
                case_result["Travel Time"] = transportation_times[facility][selected_traffic_condition]
                
                # Update bed counts for the assigned case
                bed_counts = lb.update_bed_count_for_case(case_result, bed_counts)
                logging.info(f"Case ID {case['Case ID']} assigned to {facility} with {selected_traffic_condition} traffic condition")
                break

        if not case_result["Assigned"]:
            case_result["Reason"] = "No facility has all needed bed types available."
            logging.warning(f"Case ID {case['Case ID']} could not be assigned to any facility. Reason: {case_result['Reason']}")

        case_outcomes.append(case_result)
    logging.info("Unassigned Cases: " + ", ".join([str(cid["Case ID"]) for cid in case_outcomes if not cid["Assigned"]]))
    logging.info(f"\nUpdated Bed Counts:\n{bed_counts}")
    bed_counts = bed_counts.to_dict()
    return case_outcomes, bed_counts, recs


transportation_times = {
    "Georgetown": {"Low": 40, "Medium": 45, "High": 55},
    "GWU": {"Low": 35, "Medium": 40, "High": 53},
    "Howard": {"Low": 34, "Medium": 40, "High": 50},
    "NRH": {"Low": 35, "Medium": 45, "High": 55},
    "WHC": {"Low": 35, "Medium": 44, "High": 53},
    "Sibley": {"Low": 40, "Medium": 50, "High": 63},
    "Reston": {"Low": 47, "Medium": 50, "High": 60},
    "Fauquier": {"Low": 73, "Medium": 83, "High": 105},
    "FairOaks": {"Low": 45, "Medium": 47, "High": 63},
    "FFX": {"Low": 30, "Medium": 34, "High": 40},
    "Loudoun": {"Low": 60, "Medium": 58, "High": 83},
    "MaryWash": {"Low": 68, "Medium": 77, "High": 98},
    "Mount Vernon": {"Low": 26, "Medium": 29, "High": 33},
    "Novant": {"Low": 55, "Medium": 65, "High": 93},
    "Spotsylvania": {"Low": 63, "Medium": 78, "High": 100},
    "Stafford": {"Low": 58, "Medium": 60, "High": 88},
    "VHC": {"Low": 35, "Medium": 44, "High": 50},
}

