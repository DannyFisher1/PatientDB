def is_severe(): 
    

    return 


def facility_amounts(common_results):
    facility_counts = {}

    for result in common_results:
        common_facilities = result['Common Recommended Facilities']
        for facility in common_facilities:
            if facility in facility_counts:
                facility_counts[facility] += 1
            else:
                facility_counts[facility] = 1
    facility_counts_list = [{"Facility": key, "Count": value} for key, value in facility_counts.items()]

    return sorted(facility_counts_list, key=lambda x: x["Count"], reverse=True)

