import pandas as pd

df = pd.read_csv('10981.0.csv')

lowercase_columns = df.columns = df.columns.str.lower() #convert columns name to lowercase

drop_id_duplicates = df.drop_duplicates(subset='customerid', inplace=True) #drop customerid duplicates

df['fullname'] = df['fullname'].map(lambda x:  str(x).title() if not pd.isna(x) else'unknown')

print(df.head(15))