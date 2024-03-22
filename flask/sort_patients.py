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
    critical_cases = cases
    # critical_cases = [case for case in cases if case['Severity'] == 'CRITICAL']
    logging.info(f'Amount of Critical Cases: {len(critical_cases)}')

    case_outcomes = []
    recs = []
    for case in critical_cases:
        case_result = {
            "Case ID": case['Case ID'],
            "Assigned": False,
            "Facility": None,
            "Reason": None,
            "Travel Time Ground": None,
            "Travel Time Air": None,
            "Bed Typed Needed": case['Bed Typed Needed'],
            "Trauma Level": None  # Add trauma level field
        }

        recommended_facilities = case['Common Recommended Facilities']
        facilities_times = {}
        ground_times = {}
        air_times = {}
        for facility in recommended_facilities:
            ground_time = transportation_times[facility][selected_traffic_condition]
            air_time = transportation_times[facility].get("Helicopter", None)
            trauma_level = trauma_level_dict.get(facility, 'N/A')
            facilities_times[facility] = {
                "Ground": ground_time,
                "Air": air_time if air_time is not None else "N/A",
                "Trauma Level": trauma_level 
            }
        sorted_facilities = sorted(facilities_times.items(), key=lambda x: x[1]['Ground'])
        sorted_facilities_times = {facility: times for facility, times in sorted_facilities}
        for facility in recommended_facilities:
            ground_time = transportation_times[facility][selected_traffic_condition]
            ground_times[facility] = {
                "Ground": ground_time,
            }
        sorted_ground_facilities = sorted(ground_times.items(), key=lambda x: x[1]['Ground'])
        
        for facility in recommended_facilities:
            air_time = transportation_times[facility].get("Helicopter")
            air_times[facility] = {
                "Air": air_time if air_time is not None else "N/A"
            }
        sorted_air_facilites = sorted(air_times.items(), key=lambda x: x[1]['Air'])


        recs.append({
            "Case ID": case['Case ID'],
            "Facilities": sorted_facilities_times,
            "Travel Time Ground": sorted_ground_facilities,
            "Travel Time Air": sorted_air_facilites,
            'Specialties Needed': case['Specialties Needed'],
            "Bed Types Needed": case['Bed Typed Needed'],
            "Severity": case['Severity']
        })
    return recs


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
trauma_levels = [
    {'Georgetown': 0},
    {'GWU': 1},
    {'Howard': 1},
    {'NRH': 0},
    {'WHC': 1},
    {'Sibley': 0},
    {'Reston': 2},
    {'Fauquier': 0},
    {'FairOaks': 0},
    {'FFX': 1},
    {'Loudoun': 0},
    {'MaryWash': 2},
    {'Mount Vernon': 0},
    {'Novant': 0},
    {'Spotsylvania': 0},
    {'Stafford': 0},
    {'VHC': 2}
]

trauma_level_dict = {list(level.keys())[0]: list(level.values())[0] for level in trauma_levels}