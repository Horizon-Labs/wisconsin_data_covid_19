import pandas as pd

def fetch_data():
    full_census = pd.read_csv('https://www.census.gov/content/dam/Census/topics/research/pdb2020stcov2_us.csv', encoding = "ISO-8859-1")
    wisconsin_census = full_census[full_census.State_name == 'Wisconsin']
    wisconsin_census.head(1)