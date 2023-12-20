import pandas as pd
import sqlite3

conn = sqlite3.connect('patient_cases.db' )
df = pd.read_sql_query("SELECT * FROM patient_cases", conn)
conn.close()
print(df.head()) 
