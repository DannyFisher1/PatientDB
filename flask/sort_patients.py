import random
import logging
import load_balance as lb

"""
match_patients(cases,speed)
    - take in cases and speed of traffic
    - match patients based on severity 
        - gives ground/air
        - gives active bed counts
    - returns recs 
update_facility_lists(recs,confirmed)
    - takes in recs and confirmed cases 
    - if the bed and hcf combo dont exist delete it
    - return updated recs
set_traffic_speed():
    - returns random traffic choice from transportation_times


"""


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def match_patients(cases, speed):

    selected_traffic_condition = speed
    logging.info(f"Selected traffic condition for all cases: {selected_traffic_condition}")
    # critical_cases = [case for case in cases if case['Severity'] == 'CRITICAL']
    logging.info(f'Amount of Critical Cases: {len(cases)}')

    recs = []
    for case in cases:

        recommended_facilities = case['Common Recommended Facilities']
        facilities_times = {}
        ground_times = {}
        air_times = {}
        for facility in recommended_facilities:
            ground_time = transportation_times[facility][selected_traffic_condition]
            air_time = transportation_times[facility].get("Helicopter", None)
            trauma_level = trauma_level_dict.get(facility, 'N/A')
            bed_count = lb.get_bed_num(facility, case['Bed Typed Needed'][0]) if case['Bed Typed Needed'] else 0
            bed_count = 0 if bed_count is None else bed_count
            facilities_times[facility] = {
                "Ground": ground_time,
                "Air": air_time if air_time is not None else "N/A",
                "Bed Count": bed_count,
                "Trauma Level": trauma_level,
                "Gender": case['Gender'],  # Add gender
                "Age": case['Age'],  # Add age
                "Injury ICD10_1": case['Injury ICD10_1'],  # Add injury ICD10_1
                "Injury ICD10_2": case['Injury ICD10_2'],  # Add injury ICD10_2
                "Injury ICD10_3": case['Injury ICD10_3'],  # Add injury ICD10_3
                "Injury ICD10_4": case['Injury ICD10_4'],  # Add injury ICD10_4
                "Injury AIS_1": case['Injury AIS_1'],  # Add injury AIS_1
                "Injury AIS_2": case['Injury AIS_2'],  # Add injury AIS_2
                "Injury AIS_3": case['Injury AIS_3'],  # Add injury AIS_3
                "Injury AIS_4": case['Injury AIS_4'],  # Add injury AIS_4
                "Combat Status": case['Combat Status'],  # Add combat status
                "Max ISS Score": case['Max ISS Score'],  # Add max ISS score
                "Mechanism Injury": case['Mechanism Injury'],  # Add mechanism injury
                "Primary Injury Type": case['Primary Injury Type'],  # Add primary injury type
                "Secondary Injury Type": case['Secondary Injury Type'],  # Add secondary injury type
                "Tertiary Injury Type": case['Tertiary Injury Type'],  # Add tertiary injury type
                "Medical Complications": case['Medical Complications'],  # Add medical complications
                "Disposition": case['Disposition']  # Add disposition
            }
        sorted_ground_facilities = sorted(
            facilities_times.items(),
            key=lambda x: (x[1]['Bed Count'] if x[1]['Bed Count'] is not None else 0), 
            reverse=True
        )
        sorted_facilities = sorted(facilities_times.items(), key=lambda x: x[1]['Ground'])
        sorted_facilities_times = {facility: times for facility, times in sorted_facilities}
        for facility in recommended_facilities:

            ground_time = transportation_times[facility][selected_traffic_condition]
            air_time = transportation_times[facility].get("Helicopter")
            ground_times[facility] = {
                "Ground": ground_time
            }
            air_times[facility] = {
                "Air": air_time if air_time is not None else "N/A"
            }
            
        

        if case['Severity'] == 'CRITICAL':
            sorted_ground_facilities = sorted(ground_times.items(), key=lambda x: x[1]['Ground'])
            sorted_air_facilites = sorted(air_times.items(), key=lambda x: x[1]['Air'])
        else:
            sorted_ground_facilities = sorted(facilities_times.items(), key=lambda x: x[1]['Bed Count'], reverse=True)
            sorted_air_facilites = sorted(facilities_times.items(), key=lambda x: x[1]['Bed Count'], reverse=True)

        recs.append({
            "Case ID": case['Case ID'],
            "Facilities": sorted_facilities_times,
            "Travel Time Ground": sorted_ground_facilities,
            "Travel Time Air": sorted_air_facilites,
            'Specialties Needed': case['Specialties Needed'],
            "Bed Types Needed": case['Bed Typed Needed'],
            "Severity": case['Severity'],
            "Gender": case['Gender'],  # Add gender
            "Age": case['Age'],  # Add age
            "Injury ICD10_1": case['Injury ICD10_1'],  # Add injury ICD10_1
            "Injury ICD10_2": case['Injury ICD10_2'],  # Add injury ICD10_2
            "Injury ICD10_3": case['Injury ICD10_3'],  # Add injury ICD10_3
            "Injury ICD10_4": case['Injury ICD10_4'],  # Add injury ICD10_4
            "Injury AIS_1": case['Injury AIS_1'],  # Add injury AIS_1
            "Injury AIS_2": case['Injury AIS_2'],  # Add injury AIS_2
            "Injury AIS_3": case['Injury AIS_3'],  # Add injury AIS_3
            "Injury AIS_4": case['Injury AIS_4'],  # Add injury AIS_4
            "Combat Status": case['Combat Status'],  # Add combat status
            "Max ISS Score": case['Max ISS Score'],  # Add max ISS score
            "Mechanism Injury": case['Mechanism Injury'],  # Add mechanism injury
            "Primary Injury Type": case['Primary Injury Type'],  # Add primary injury type
            "Secondary Injury Type": case['Secondary Injury Type'],  # Add secondary injury type
            "Tertiary Injury Type": case['Tertiary Injury Type'],  # Add tertiary injury type
            "Medical Complications": case['Medical Complications'],  # Add medical complications
            "Disposition": case['Disposition']  # Add disposition
        })
    return recs


def update_facility_lists(recs, confirmed):
    unmatched_results = []

    for rec in recs:
        rec['is_confirmed'] = any(int(rec['Case ID']) == int(conf['case_id']) for conf in confirmed)
        for conf in confirmed:
            if int(rec['Case ID']) == int(conf['case_id']):
                rec['confirmed_facility'] = conf['facility']
                rec['mode'] = conf['mode']
                rec['time'] = conf['time']
                break

        facilities_to_remove = []

       
        for transport_mode in ['Travel Time Ground', 'Travel Time Air']:
            for facility, _ in rec[transport_mode]:
                for bed_type in rec['Bed Types Needed']:
                    if not lb.check_beds(facility, bed_type):
                        if facility not in facilities_to_remove: 
                            facilities_to_remove.append(facility)
                            print(f'Not available in {transport_mode}: {facility} {bed_type}')
            

  
        rec['Travel Time Ground'] = [(facility, details) for facility, details in rec['Travel Time Ground'] if facility not in facilities_to_remove]
        rec['Travel Time Air'] = [(facility, details) for facility, details in rec['Travel Time Air'] if facility not in facilities_to_remove]
        if not rec['Travel Time Ground'] and not rec['Travel Time Air']:
            unmatched_results.append(rec)
    recs = [rec for rec in recs if rec not in unmatched_results]

    return recs, unmatched_results

def set_traffic_speed():
        return random.choice(['Low', 'Medium', 'High'])

transportation_times = {
    "Georgetown": {"Low": 40, "Medium": 45, "High": 55, "Helicopter": 13.10},
    "GWU": {"Low": 35, "Medium": 40, "High": 53, "Helicopter": 13.30},
    "Howard": {"Low": 34, "Medium": 40, "High": 50, "Helicopter": 0.00},
    "NRH": {"Low": 35, "Medium": 45, "High": 55, "Helicopter": 0.00},
    "WHC": {"Low": 35, "Medium": 44, "High": 53, "Helicopter": 12.78},
    "Sibley": {"Low": 40, "Medium": 50, "High": 63, "Helicopter": 14.76},
    "Reston": {"Low": 47, "Medium": 50, "High": 60, "Helicopter": 21.16},
    "Fauquier": {"Low": 73, "Medium": 83, "High": 105, "Helicopter": 32.10},
    "FairOaks": {"Low": 45, "Medium": 47, "High": 63, "Helicopter": 20.70},
    "FFX": {"Low": 30, "Medium": 34, "High": 40, "Helicopter": 16.50},
    "Loudoun": {"Low": 60, "Medium": 58, "High": 83, "Helicopter": 25.61},
    "MaryWash": {"Low": 68, "Medium": 77, "High": 98, "Helicopter": 30.32},
    "Mount Vernon": {"Low": 26, "Medium": 29, "High": 33, "Helicopter": 12.57},
    "Novant": {"Low": 55, "Medium": 65, "High": 93, "Helicopter": 23.29},
    "Spotsylvania": {"Low": 63, "Medium": 78, "High": 100, "Helicopter": 32.96},
    "Stafford": {"Low": 58, "Medium": 60, "High": 88, "Helicopter": 26.41},
    "VHC": {"Low": 35, "Medium": 44, "High": 50, "Helicopter": 0.00}
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