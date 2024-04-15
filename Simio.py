import pandas as pd
import convert_patient_data as cpd 
import cases_func as cf 
import cases 

# Load the data
data = cpd.get_data('uploads/New_cases_0223.xlsx')

# Get the matched case information
matched_info = cf.get_info(data)

# Add bed hours to matched_info
matched_df = pd.DataFrame(matched_info)
matched_df[['first_bed_hours', 'second_bed_hours', 'third_bed_hours']] = data[['first_bed_hours', 'second_bed_hours', 'third_bed_hours']]

# Create a new Excel writer object
writer = pd.ExcelWriter('cases_facilities.xlsx', engine='xlsxwriter')

# Function to generate bed types and hours for each facility
def get_bed_types_and_hours(row):
    bed_types = row['Bed Typed Needed'] + ['Post_Acute_Care']  # Add 'Post_Acute_Care' here
    bed_hours = row[['first_bed_hours', 'second_bed_hours', 'third_bed_hours']].tolist() + [0]  # Add 0 hours for 'Post_Acute_Care' here
    bed_types_and_hours = dict(zip(bed_types, bed_hours))
    return bed_types_and_hours

# Iterate over each case in the matched data
for index, row in matched_df.iterrows():
    case_id = f"case{int(row['Case ID']):03d}"  # Format the case ID
    facilities = row['Common Recommended Facilities']
    bed_types_and_hours = get_bed_types_and_hours(row)
    
    # Iterate over each facility and create a separate sheet
    for facility in facilities:
        # Initialize a list to store the data for this facility
        facility_data = []
        
        # Create data for each bed type and its corresponding hours
        for bed_type, hours in bed_types_and_hours.items():
            # The final entry should not include the facility name for 'Post_Acute_Care'
            facility_identifier = facility if bed_type != 'Post_Acute_Care' else ''
            sequence_name = f'Input@{facility_identifier}_{bed_type.replace(" ", "_")}' if facility_identifier else 'Input@Post_Acute_Care'
            # Set process time to 0 if the bed type is 'Post_Acute_Care'
            process_time = hours if bed_type != 'Post_Acute_Care' else 0
            facility_data.append({
                'Sequence': sequence_name,
                'ProcessTime': process_time
            })
        
        # Convert the data to a DataFrame
        df_facility = pd.DataFrame(facility_data)
        
        # Write the dataframe to a specific sheet named by case and facility
        df_facility.to_excel(writer, sheet_name=f"{case_id}_{facility}", index=False)
        
        # Get the workbook and the worksheet objects to apply formatting
        workbook = writer.book
        worksheet = writer.sheets[f"{case_id}_{facility}"]
        
        # Set the column widths
        worksheet.set_column('A:A', 30)  # Set width of column A
        worksheet.set_column('B:B', 20)  # Set width of column B
        
        # Write the headers
        worksheet.write('A1', 'Sequence')
        worksheet.write('B1', 'ProcessTime')

# Save the Excel file
writer._save()
