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

# Note: Ensure you have an `update_bed_count_for_case` function in your `lb` module that correctly updates bed counts.
# Mock load_balance module content
class load_balance:
    data = {
        'Bed Type': ['ICU', 'ICU', 'General', 'General', 'Emergency', 'Emergency'],
        'Georgetown': [2, 3, 5, 5, 1, 2],
        'GWU': [3, 2, 4, 4, 3, 1],
        # Add similar data for other facilities...
    }

    @staticmethod
    def update_bed_count_for_case(case, bed_counts, facility):
        # Simplified mock-up: Decrease the count of the needed bed type by 1
        for bed_type in case['Bed Typed Needed']:
            bed_counts[bed_type][facility] -= 1
        return bed_counts

# Example critical cases
cases = [
    {
        'Case ID': 1,
        'Severity': 'CRITICAL',
        'Common Recommended Facilities': ['Georgetown', 'GWU'],
        'Bed Typed Needed': ['ICU'],
        'Specialties Needed': ['Cardiology']
    },
    {
        'Case ID': 2,
        'Severity': 'CRITICAL',
        'Common Recommended Facilities': ['Georgetown', 'GWU'],
        'Bed Typed Needed': ['General'],
        'Specialties Needed': ['Neurology']
    },
    # Add more cases as needed...
]

# Assuming the get_crit_facilities function is already defined as per the earlier instructions...

# Print sample outputs
case_outcomes, updated_bed_counts, recs = get_crit_facilities(cases)

print("Case Outcomes:", case_outcomes)
print("\nUpdated Bed Counts:", updated_bed_counts)
print("\nRecommendations:", recs)