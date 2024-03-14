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
            "Bed Typed Needed": case['Bed Typed Needed']
        }

        recommended_facilities = case['Common Recommended Facilities']
        facilities_times = {}
        for facility in recommended_facilities:
            ground_time = transportation_times[facility][selected_traffic_condition]
            air_time = transportation_times[facility].get("Helicopter", None)
            facilities_times[facility] = {
                "Ground": ground_time,
                "Air": air_time if air_time is not None else "N/A"  # Represent air time distinctly, handle facilities without helicopter access
            }
        
        recs.append({
            "Case ID": case['Case ID'],
            "Facilities": facilities_times,  # Now contains separate entries for ground and air travel times
            'Specialties Needed': case['Specialties Needed'],
            "Bed Types Needed": case['Bed Typed Needed']
        })

        # Here we continue with the logic of assigning facilities based on ground transportation and bed availability
        for facility, times in facilities_times.items():
            needed_bed_types = case['Bed Typed Needed']
            if all(bed_counts.loc[bed_type, facility] > 0 for bed_type in needed_bed_types):
                case_result["Assigned"] = True
                case_result["Facility"] = facility
                case_result["Travel Time"] = times["Ground"]  # Using ground travel time for assignments
                
                bed_counts = lb.update_bed_count_for_case(case_result, bed_counts)
                logging.info(f"Case ID {case['Case ID']} assigned to {facility} with ground travel time of {times['Ground']} minutes.")
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
    "Georgetown": {"Low": 40, "Medium": 45, "High": 55, "Helicopter": 13.095},
    "GWU": {"Low": 35, "Medium": 40, "High": 53, "Helicopter": 13.295},
    "Howard": {"Low": 34, "Medium": 40, "High": 50, "Helicopter": 0},
    "NRH": {"Low": 35, "Medium": 45, "High": 55, "Helicopter": 0},
    "WHC": {"Low": 35, "Medium": 44, "High": 53, "Helicopter": 12.78},
    "Sibley": {"Low": 40, "Medium": 50, "High": 63, "Helicopter": 14.76},
    "Reston": {"Low": 47, "Medium": 50, "High": 60, "Helicopter": 21.155},
    "Fauquier": {"Low": 73, "Medium": 83, "High": 105, "Helicopter": 32.1},
    "FairOaks": {"Low": 45, "Medium": 47, "High": 63, "Helicopter": 20.7},
    "FFX": {"Low": 30, "Medium": 34, "High": 40, "Helicopter": 16.5},
    "Loudoun": {"Low": 60, "Medium": 58, "High": 83, "Helicopter": 25.61},
    "MaryWash": {"Low": 68, "Medium": 77, "High": 98, "Helicopter": 30.315},
    "Mount Vernon": {"Low": 26, "Medium": 29, "High": 33, "Helicopter": 12.565},
    "Novant": {"Low": 55, "Medium": 65, "High": 93, "Helicopter": 23.29},
    "Spotsylvania": {"Low": 63, "Medium": 78, "High": 100, "Helicopter": 32.955},
    "Stafford": {"Low": 58, "Medium": 60, "High": 88, "Helicopter": 26.41},
    "VHC": {"Low": 35, "Medium": 44, "High": 50, "Helicopter": 0},
}
