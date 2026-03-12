import pandas as pd
import sqlite3 
df = pd.read_csv('job_liss.csv')

#print(df.head(20).to_string())

#print(df.head(20).dropna().to_string())


sqlite_connection = sqlite3.connect('job_list.db')



# Clean whitespace, lowercase, and fix multi-word spaces, but PROTECT the comma
df['required_skills'] = df['required_skills'].str.lower().str.replace(', ', ',').str.replace(' ', '_').str.replace(',',' ')

df.to_sql('job_list', sqlite_connection, if_exists='replace', index=False)

