import pandas as pd
import sqlite3

conn = sqlite3.connect('patient_cases.db' )
query = "SELECT * FROM patient_cases WHERE case_id > 25;"
df = pd.read_sql_query(query, conn)

cleaned = df[[
    "case_id", "arrival_severity",
    "first_bed_type", "first_bed_hours",
    "second_bed_type", "second_bed_hours", 
    "third_bed_type", "third_bed_hours", 
    "fourth_bed_type", "fourth_bed_hours", 
    "fifth_bed_type", "fifth_bed_hours", 
    "sixth_bed_type", "sixth_bed_hours", 
    "seventh_bed_type", "seventh_bed_hours", 
    "eighth_bed_type", "eighth_bed_hours", 
    "ninth_bed_type", "ninth_bed_hours", 
    "tenth_bed_type", "tenth_bed_hours"
]]
conn.close()
print(cleaned.iloc[75]) 
cleaned.to_csv("cleaned_patient_data.csv", index = False)
df.to_csv("patient_data.csv", index = False)