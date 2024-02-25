import pandas as pd
from cases_funct import  match_bed, match_spec

def get_info(df): 
    beds = match_bed(df)
    specs = match_spec(df)
    results = find_common_facilities(beds,specs)
    return results


def find_common_facilities(beds, specs):
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
        return common_results






