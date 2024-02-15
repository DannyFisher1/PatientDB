import pandas as pd
def process_excel_file(input_file_path, output_file_path):
    # Load the Excel file
    xls = pd.ExcelFile(input_file_path)
    
    # Writer object to save the modified Excel file
    writer = pd.ExcelWriter(output_file_path, engine='openpyxl')
    
    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(input_file_path, sheet_name=sheet_name)
        
        # Modify the 'Sequence' column to remove the facility name for specific entries
        df['Sequence'] = df['Sequence'].str.replace(r'(.*)@(.*)_Post_Acute_Care', r'Input@Post_Acute_Care', regex=True)
        
        # Write the modified DataFrame to the new Excel file under the same sheet name
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Save the new Excel file
    writer._save()
    writer.close()

# Specify the input and output file paths
input_file_path = 'Case Data.xlsx'
output_file_path = 'Case_data_modified.xlsx'

# Call the function with the specified file paths
process_excel_file(input_file_path, output_file_path)

print("Excel file has been processed and saved.")
