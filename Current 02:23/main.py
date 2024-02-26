from Convert_Patient_data import get_data
from cases import get_info
from cases_funct import facility_amounts

if __name__ == '__main__':
    workbook_path = 'New cases 0223.xlsx'
    data = get_data(workbook_path)
    df =  get_info(data)
    
    print(facility_amounts(df))
