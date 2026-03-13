import pandas as pd
import re #for regex matching
from thefuzz import process #for spelling matching

#this function will check the spelling and if its close enought to the correct words
# it  will return the correct version
def check_spelling(word, correct_words=['Free', 'Premium', 'Basic']):
    
    # if the word is null return free as default value
    if pd.isna(word):
        return 'Free'
    
    #this is fuzz in action it will compare the likelyness of the current word to the correct one and
    #will return score as a probability and fuzz_result as the most likely correct word
    fuzz_result, score  = process.extractOne(word, correct_words)

    if score >= 80:
        return fuzz_result
    else:
        return 'free'
    
    
df = pd.read_csv('10981.0.csv')

#convert columns name to lowercase
lowercase_columns = df.columns = df.columns.str.lower() 

#drop customerid duplicates
drop_id_duplicates = df.drop_duplicates(subset='customerid', inplace=True) 

#format username and if its null make it unknown
df['fullname'] = df['fullname'].map(lambda x:  str(x).strip().title() if not pd.isna(x) else'unknown') 

#using re we match the regex to each email value
#i use re match for conditional
valid_email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
df['email'] = df['email'].str.strip()
df['email'] = df['email'].map(lambda x: str(x).lower() if re.match(valid_email_pattern, str(x)) else 'invalid@gmail.com') 

#strip the phone value to core until only 7 digits left and also while making sure that its valid phone number also converting invalid phone to 000-0000
#i use regex sub here to format the phone and \D to remove non digit character and also check if the length is 7 and not null to make sure its valid phone number
df['phone'] = df['phone'].str.strip().str.replace('+1','').str.replace('(','').str.replace(')','').str.replace('-','').str.replace(' ','').str.replace(r'[a-zA-Z]', '', regex=True)
df['phone'] = df['phone'].map(lambda x: re.sub(r'\D', '', str(x)) if len(str(x)) == 7 and not pd.isna(x) else '000-0000')

#in computing the mean i use the built mean function but before that i use to_numeric which is necessary to convert non numerical value
#nan and also convert the string value to int or float
#so after changing the non numeric data i make a condition and use between method to get the qualified value for median computation
#in the final output i jsut use lamda to loop to each and change the value to mean age
median_age = int(pd.to_numeric(df['age'], errors='coerce')[pd.to_numeric(df['age'], errors='coerce').between(18, 120)].median())
df['age'] = df['age'].map(lambda x: x if pd.to_numeric(x, errors='coerce') >= 18 and pd.to_numeric(x, errors='coerce') <= 120 else median_age)

#to format the date i did a minor cleaning first converting / to - and remove spaces
#and on second phase i use to_datetime with format mixed since the data is super messy because there are 
#date that in text form and wrong format overall so i used mixed instead of strict format like %Y-%m-%d or %d-%m-%Y 
# and ofcourse add errors coerce to convert the invalid date to NaT and not throw error and stop the program
df['joindate'] = df['joindate'].str.strip().str.replace('/','-', regex=False)
df['joindate']  = pd.to_datetime(df['joindate'],format='mixed', errors='coerce')

#so i use apply to call the function that contain the spell check process in each value 
# and convert it to title since that is the correct format
df['subtier'] = df['subtier'].apply(check_spelling).str.title()

print(df.head(15))