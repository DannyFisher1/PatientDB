import random
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

transportation_times = {
    "Georgetown": {"Low": 40, "Medium": 45, "High": 55, "Helicopter": 13.095},
    "GWU": {"Low": 35, "Medium": 40, "High": 53, "Helicopter": 13.295},
    "Howard": {"Low": 34, "Medium": 40, "High": 50, "Helicopter": 0},
    # Add remaining facilities with their transportation times including Helicopter times
}

def get_crit_facilities(cases):
    bed_counts = pd.DataFrame(load_balance.data).set_index('Bed Type')
    
    selected_traffic_condition = random.choice(['Low', 'Medium', 'High'])
    logging.info(f"Selected traffic condition for all cases: {selected_traffic_condition}")

    critical_cases = [case for case in cases if case['Severity'] == 'CRITICAL']
    logging.info(f'Amount of Critical Cases: {len(critical_cases)}')

    case_outcomes = []
    recs = []
    for case in critical_cases:
        recommended_facilities = case['Common Recommended Facilities']
        facilities_times = {facility: transportation_times[facility] for facility in recommended_facilities}
        for facility, times in facilities_times.items():
            times['Helicopter'] = times.get('Helicopter', float('inf'))  # Use infinity as default if no helicopter time

        sorted_facilities = sorted(facilities_times, key=lambda x: min(facilities_times[x].values()))
        recs.append({
            "Case ID": case['Case ID'],
            "Facility Times": {facility: {cond: times for cond, times in facilities_times[facility].items() if cond in ['Low', 'Medium', 'High', 'Helicopter']} for facility in sorted_facilities},
            'Specialties Needed': case['Specialties Needed'],
            "Bed Types Needed": case['Bed Typed Needed']
        })

        for facility in sorted_facilities:
            needed_bed_types = case['Bed Typed Needed']
            if all(bed_counts.loc[bed_type, facility] > 0 for bed_type in needed_bed_types):
                shortest_travel_time = min(facilities_times[facility].values())
                case_outcomes.append({
                    "Case ID": case['Case ID'],
                    "Assigned": True,
                    "Facility": facility,
                    "Travel Time": shortest_travel_time,
                    "Bed Typed Needed": case['Bed Typed Needed']
                })
                # Update bed counts for the assigned case (implement this in `lb.update_bed_count_for_case`)
                bed_counts = load_balance.update_bed_count_for_case(case, bed_counts, facility)
                logging.info(f"Case ID {case['Case ID']} assigned to {facility} with travel time {shortest_travel_time}")
                break
        else:
            case_outcomes.append({
                "Case ID": case['Case ID'],
                "Assigned": False,
                "Reason": "No facility has all needed bed types available."
            })
            logging.warning(f"Case ID {case['Case ID']} could not be assigned to any facility. Reason: No facility has all needed bed types available.")

    logging.info("Unassigned Cases: " + ", ".join([str(cid["Case ID"]) for cid in case_outcomes if not cid["Assigned"]]))
    return case_outcomes, bed_counts.to_dict(), recs

    #     for facility, times in facilities_times.items():
    #         needed_bed_types = case['Bed Typed Needed']
    #         # Check if the first needed bed type requires trauma level consideration
    #         if needed_bed_types[0] in ['Med/Surg', 'ICU/Critical Care']:
    #             trauma_level = trauma_level_dict.get(facility, None)
    #             # Convert trauma level to "L1" or "L2"
    #             if trauma_level is not None:
    #                 case_result["Trauma Level"] = "L1" if trauma_level == 1 else "L2"

    #         if all(bed_counts.loc[bed_type, facility] > 0 for bed_type in needed_bed_types):
    #             case_result["Assigned"] = True
    #             case_result["Facility"] = facility
    #             case_result["Travel Time"] = times["Ground"]
    #             bed_counts = lb.update_bed_count_for_case(case_result, bed_counts)
    #             logging.info(f"Case ID {case['Case ID']} assigned to {facility} with ground travel time of {times['Ground']} minutes and trauma level {case_result['Trauma Level']}.")
    #             break

    #     if not case_result["Assigned"]:
    #         case_result["Reason"] = "No facility has all needed bed types available."
    #         logging.warning(f"Case ID {case['Case ID']} could not be assigned to any facility. Reason: {case_result['Reason']}")

    #     case_outcomes.append(case_result)

    # logging.info("Unassigned Cases: " + ", ".join([str(cid["Case ID"]) for cid in case_outcomes if not cid["Assigned"]]))
    # logging.info(f"\nUpdated Bed Counts:\n{bed_counts}")
    # bed_counts = bed_counts.to_dict()

    # return case_outcomes, bed_counts, recs