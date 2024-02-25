import pandas as pd

# Path to your original Excel file
#Charactoristics .xlsx
file_path = 'Charactoristics .xlsx'

# Services list as provided
services_list = [
    "Trauma Surgery", "Cardiothoracic Surgery", "Orthopedic Surgery",
    "Neurosurgery", "Vascular Surgery", "Interventional radiology",
    "Maxillofacial Reconstructive", "Otolaryngology_ENT", "Urology", "General Surgery", "Ophthalmology_Trauma",
    "Plastic Surgery_Reconstructive", "Psychiatry", "Internal Medicine",
    "Infectious Disease", "Neurology", "Cardiology", "Nephrology", "Pulmonology",
    "Intensive_Daily_OT", "Intensive_Daily_PT", "Prosthetics", "Neuro Rehab",
    "Orthopedics Rehab", "Mental_Health_Services _(Counseling)",
    "Mental_Health_Services _(Counseling)", "Visiting Nurse", "Home_Health_Aid_(ADL)",
    "Wound Services", "Dialysis_Services", "Infusion_Services", "Pain_Management_Services",
    "Surgical_Center_Services", "Other_Rehab"
]

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Initialize matrix data with 'Specialty' as keys
matrix_data = {"Specialty": services_list}

# Function to normalize service names for better matching
def normalize_service_name(name):
    return name.split('-')[0]

# Normalize the services list
normalized_services_list = [normalize_service_name(name) for name in services_list]

# Iterate through each sheet and fill in the matrix
for sheet_name in xls.sheet_names:
    df_sheet = pd.read_excel(xls, sheet_name, skiprows=62, nrows=51, usecols="A:B")
    # Normalize the service names in the sheet
    df_sheet.iloc[:, 0] = df_sheet.iloc[:, 0].apply(normalize_service_name)
    availability = []
    for service in normalized_services_list:
        # Check if the normalized service name is present and marked 'Yes'
        service_availability = df_sheet[(df_sheet.iloc[:, 0] == service) & (df_sheet.iloc[:, 1] == 'Yes')].shape[0] > 0
        availability.append(1 if service_availability else 0)
    matrix_data[sheet_name.split('-')[0]] = availability

# Convert the dictionary to a DataFrame
df_matrix = pd.DataFrame(matrix_data)
df_matrix.set_index('Specialty', inplace=True)

# Save the matrix to an Excel file
output_file_path = 'specialty_availability_matrix.xlsx'
df_matrix.to_excel(output_file_path)
df_matrix.to_csv("data_matrix.csv", index = False)

print(f"Matrix saved to {output_file_path}")
