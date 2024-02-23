from Convert_Patient_data import get_data
from cases import get_info

if __name__ == '__main__':
    workbook_path = 'New cases 0223.xlsx'
    df = get_data(workbook_path)
    get_info(df)
