import pandas as pd
import sqlite3

df = pd.read_csv('job_list.csv')

df.insert(0, 'id', range(1, len(df) + 1))


def salary_cleaner(salary_column):
    if 'k' in salary_column:
        return int(salary_column.replace('k', '').strip()) * 1000  
    elif 'M' in salary_column:
        return int(float(salary_column.replace('M', '').strip()) * 1000000)
    else:
        return int(salary_column.strip())
    
def salary_splitter(country, entry, mid, senior):
    salaries = df[country].str.split("|", expand=True)
    for index in range(len(salaries.columns)):
        if index == 0:
            df[entry] = salaries[index].str.strip().str.replace('Entry:', '')
            df[entry] = df[entry].apply(salary_cleaner)
        elif index == 1:
            df[mid] = salaries[index].str.strip().str.replace('Mid:', '')
            df[mid] = df[mid].apply(salary_cleaner)
        elif index == 2:
            df[senior] = salaries[index].str.strip().str.replace('Senior:', '')
            df[senior] = df[senior].apply(salary_cleaner)
 
def clean_skills(skills_column):
    clean = ''
    for skill in skills_column.split(','):
        clean += f"|{skill.strip()}| "
    return clean

salary_splitter('salary_ph_php', 'salary_ph_entry', 'salary_ph_mid', 'salary_ph_senior') 
salary_splitter('salary_us_usd', 'salary_us_entry', 'salary_us_mid', 'salary_us_senior')   
salary_splitter('salary_uk_gbp', 'salary_uk_entry', 'salary_uk_mid', 'salary_uk_senior')    

df.drop(columns=['salary_ph_php', 'salary_us_usd', 'salary_uk_gbp'], inplace=True) 

df['required_skills'] = df['required_skills'].str.strip().apply(clean_skills)
df['related_words'] = df['related_words'].str.strip().apply(clean_skills)
df['tools_used'] = df['tools_used'].str.strip().apply(clean_skills)



df['learning_roadmap'] = df['learning_roadmap'].str.strip().str.replace('|', '; ')
df['roadmap_with_study_links'] = df['roadmap_with_study_links'].str.strip().str.replace('|', ';')
df['common_interview_questions'] = df['common_interview_questions'].str.strip().str.replace('|', ';')

df = df[[
    'id',                       
    'job_title',
    'specialization',
    'difficulty',
    'future_career_projection',
    'salary_ph_entry',
    'salary_ph_mid',
    'salary_ph_senior',
    'salary_us_entry',
    'salary_us_mid',
    'salary_us_senior',
    'salary_uk_entry',
    'salary_uk_mid',
    'salary_uk_senior',
    'remote_work_viability',
    'detailed_overview',
    'job_guide_link',
    'required_skills',
    'tools_used',
    'learning_roadmap',
    'roadmap_with_study_links',
    'common_interview_questions',
    'related_careers',
    'time_to_master',
    'related_words',
    'resume_project_idea',
    'work_life_balance',
    'suggested_certifications',
    'degree_necessity'
]]

print(df.head()['required_skills'])

conn = sqlite3.connect('job_list.db')
df.to_sql('job_list', conn, if_exists='replace', index=False)