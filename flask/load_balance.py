import logging
from flask import session

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

def change(beds):
    beds = {facility: {data["Bed Type"][i]: counts[i] for i in range(len(data["Bed Type"]))} for facility, counts in data.items() if facility != "Bed Type"}

def update_beds(placement):
    if 'bd' not in session:
        session['bd'] = data
    
    beds_data = session['bd']
    facility = placement['facility']
    bed_type = placement['bedType']
    
    if facility in beds_data:
        bed_index = beds_data["Bed Type"].index(bed_type)
        if beds_data[facility][bed_index] > 0:
            print(f"Before update: {beds_data[facility][bed_index]} available beds of type {bed_type} at {facility}")
            beds_data[facility][bed_index] -= 1
            print(f"After update: {beds_data[facility][bed_index]} available beds of type {bed_type} at {facility}")
            session['bd'] = beds_data  # Update the session with the modified counts
            session.modified = True
    else:
        print("Facility not found in the data.")

def check_beds(facility, bed_type):
    if 'bd' not in session:
        session['bd'] = data  
    beds_data = session['bd']
    if facility in beds_data:
        bed_index = beds_data["Bed Type"].index(bed_type)
        if beds_data[facility][bed_index] > 0:
           return True
    else:
        return False


# Check bed percents 
# if bed.space >x% total space: 
# pass 
# switch facilities 