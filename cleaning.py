import pandas as pd
import re #for regex matching

df = pd.read_csv('10981.0.csv')

#convert columns name to lowercase
lowercase_columns = df.columns = df.columns.str.lower() 

#drop customerid duplicates
drop_id_duplicates = df.drop_duplicates(subset='customerid', inplace=True) 

#format username and if its null make it unknown
df['fullname'] = df['fullname'].map(lambda x:  str(x).title() if not pd.isna(x) else'unknown') 

#using re we match the regex to each email value
#i use re match for conditional
valid_email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
df['email'] = df['email'].str.strip().str.replace('.','')
df['email'] = df['email'].map(lambda x: str(x).lower() if re.match(valid_email_pattern, str(x)) else 'invalid@email.com') 

#strip the phone value to core until only 8 digits left and also while making sure that its valid phone number also converting invalid phone to 000-0000
#i use regex sub here to format the phone 
valid_phone_pattern = r'^(\d{3})(\d{4})$'
df['phone'] = df['phone'].str.strip().str.replace('+1','').str.replace('(','').str.replace(')','').str.replace('-','').str.replace(' ','').str.replace(r'[a-zA-Z]', '', regex=True)
df['phone'] = df['phone'].map(lambda x: re.sub(valid_phone_pattern,r'\1-\2', str(x)) if len(str(x)) == 7 and not pd.isna(x) else '000-0000')

#in computing the mean i use the built mean function but before that i use to_numeric which is necessary to convert non numerical value
#nan and also convert the string value to int or float
#so after changing the non numeric data i make a condition and use between method to get the qualified value for median computation
#in the final output i jsut use lamda to loop to each and change the value to mean age
mean_age = int(pd.to_numeric(df['age'], errors='coerce')[pd.to_numeric(df['age'], errors='coerce').between(18, 120)].median())
df['age'] = df['age'].map(lambda x: x if pd.to_numeric(x, errors='coerce') >= 18 and pd.to_numeric(x, errors='coerce') <= 120 else mean_age)



print(df.head(15))