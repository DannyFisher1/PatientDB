from flask import session

data = {
    "Bed Type": ["Med/Surg", "ICU/Critical Care", "Psych", "Post_Acute_Care", "Burn", "Burn ICU", "Isolation", "Acute Rehabilitation Unit (ARU)"],
    "Georgetown": [12, 3, 1, 0, 0, 0, 0, 2],
    "GWU": [12, 3, 1, 1, 0, 0, 1, 1],
    "Howard": [14, 1, 1, 0, 0, 0, 1, 0],
    "NRH": [0, 0, 0, 0, 0, 0, 0, 7],
    "WHC": [29, 6, 2, 1, 1, 1, 1, 0],
    "Sibley": [9, 1, 1, 0, 0, 0, 1, 1],
    "Reston": [7, 1, 0, 0, 0, 0, 1, 1],
    "Fauquier": [3, 1, 0, 1, 0, 0, 1, 0],
    "FairOaks": [5, 1, 0, 1, 0, 0, 1, 0],
    "FFX": [27, 5, 2, 0, 0, 0, 6, 0],
    "Loudoun": [6, 1, 1, 2, 0, 0, 1, 0],
    "MaryWash": [14, 2, 4, 1, 0, 0, 0, 1],
    "Mount Vernon": [5, 1, 2, 3, 0, 0, 1, 1],
    "Novant": [3, 1, 2, 1, 0, 0, 0, 1],
    "Spotsylvania": [2, 1, 2, 1, 0, 0, 1, 0],
    "Stafford": [2, 1, 0, 2, 0, 0, 0, 0],
    "VHC": [9, 2, 1, 1, 0, 0, 1, 1]
    }

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
    
def get_bed_num(facility, bed_type):
    if 'bd' not in session:
        session['bd'] = data  
    beds_data = session['bd']

    if facility in beds_data:
        bed_index = beds_data["Bed Type"].index(bed_type)
        if beds_data[facility][bed_index] > 0:
           return beds_data[facility][bed_index]
    else:
        return 0


# Check bed percents 
# if bed.space >x% total space: 
# pass 
# switch facilities 