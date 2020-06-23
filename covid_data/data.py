import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import random
import os.path
from os import path
import time
import threading

wisconsin_census = None
covid_cases = None
vaccinated = None
counties = ['Adams','Ashland','Barron','Bayfield','Brown','Buffalo','Burnett','Calumet','Chippewa','Clark','Columbia','Crawford','Dane','Dodge','Door','Douglas','Dunn','Eau Claire','Florence','Fond du Lac','Forest','Grant','Green','Green Lake','Iowa','Iron','Jackson','Jefferson','Juneau','Kenosha','Kewaunee','La Crosse','Lafayette','Langlade','Lincoln','Manitowoc','Marathon','Marinette','Marquette','Menominee','Milwaukee','Monroe','Oconto','Oneida','Outagamie','Ozaukee','Pepin','Pierce','Polk','Portage','Price','Racine','Richland','Rock','Rusk','St. Croix','Sauk','Sawyer','Shawano','Sheboygan','Taylor','Trempealeau','Vernon','Vilas','Walworth','Washburn','Washington','Waukesha','Waupaca','Waushara','Winnebago','Wood']
codes = [55001,55003,55005,55007,55009,55011,55013,55015,55017,55019,55021,55023,55025,55027,55029,55031,55033,55035,55037,55039,55041,55043,55045,55047,55049,55051,55053,55055,55057,55059,55061,55063,55065,55067,55069,55071,55073,55075,55077,55078,55079,55081,55083,55085,55087,55089,55091,55093,55095,55097,55099,55101,55103,55105,55107,55109,55111,55113,55115,55117,55119,55121,55123,55125,55127,55129,55131,55133,55135,55137,55139,55141]

def fetch_census(cache="census.csv", force_update=False):
    global wisconsin_census
    if not force_update and path.exists(cache):
        wisconsin_census = pd.read_csv(cache)
    else:
        full_census = pd.read_csv('https://www.census.gov/content/dam/Census/topics/research/pdb2020stcov2_us.csv', encoding = "ISO-8859-1", skiprows=[1])
        wisconsin_census = full_census[full_census.State_name == 'Wisconsin']
        wisconsin_census = wisconsin_census[wisconsin_census.Geog_Level == 'County']

        wisconsin_census.rename(columns={'GIDSTCO': 'fips', 'county': 'county_number', 'County_name': 'county', 'LAND_AREA': 'area', 'Tot_Population_ACS_14_18': 'population', 'Males_ACS_14_18': 'male_population', 'Females_ACS_14_18': 'female_population', 'Median_Age_ACS_14_18': 'median_age', 'Pop_under_5_ACS_14_18': '<5', 'Pop_5_17_ACS_14_18':'5-17', 'Pop_18_24_ACS_18_24': '18-24', 'Pop_25_44_ACS_14_18': '25-44', 'Pop_45_64_ACS_14_18': '45-64', 'Pop_65plus_ACS_14_18': '65+'})

        for i in range(len(wisconsin_census['county'])):
            wisconsin_census['county'][i] = wisconsin_census['county'][i][:-7] 

        wisconsin_census.to_csv(cache)
        wisconsin_census = pd.read_csv(cache)
    return wisconsin_census

def fetch_cases(cache="covid_cases.csv", force_update=False, day=datetime.strftime(datetime.now() - timedelta(1), '%Y/%m/%d') ):
    global covid_cases
    if not force_update and path.exists(cache):
        covid_cases = pd.read_csv(cache)
    else:
        cases_request = requests.get('https://opendata.arcgis.com/datasets/b913e9591eae4912b33dc5b4e88646c5_10.geojson')
        cases_res = json.loads(cases_request.content)
        cases_data = {}
        for k in cases_res['features'][0]['properties'].keys():
            cases_data[k] = []

        for feature in cases_res['features']:
            if feature['properties']['DATE'][:10] == day and feature['properties']['GEO'] == "County":
                for k in feature['properties'].keys():
                    cases_data[k].append(feature['properties'][k])
        covid_cases = pd.DataFrame(data=cases_data)

        covid_cases.rename(columns={'GEOID': 'fips', 'NAME': 'county'})

        covid_cases.to_csv(cache)
    return covid_cases

def fetch_vaccinations(cache="vaccinated.csv", force_update=False, vaccinations_file="vaccinations.csv"):
    # temp make random data
    global vaccinated
    global codes
    if not force_update and path.exists(cache):
        vaccinated = pd.read_csv(cache)
    else:
        if not force_update and path.exists(vaccinations_file):
            countyVaccines = {}

            vaccinations = pd.read_csv(vaccinations_file)

            for county in codes:
                countyVaccines[county] = {'total': 0, 'male': 0, 'female': 0, '<5': 0, '5-17': 0, '18-24': 0, '25-44': 0, '45-64': 0, '65+': 0}

            for i in range(len(vaccinations['fips'])):
                countyVaccines[vaccinations['fips'][i]]['total'] += 1

                if vaccinations['gender'][i] == 'male':
                    countyVaccines[vaccinations['fips'][i]]['male'] += 1
                elif vaccinations['gender'][i] == 'female':
                    countyVaccines[vaccinations['fips'][i]]['female'] += 1

                if vaccinations['age'][i] < 5:
                    countyVaccines[vaccinations['fips'][i]]['<5'] += 1
                elif vaccinations['age'][i] < 18:
                    countyVaccines[vaccinations['fips'][i]]['5-17'] += 1
                elif vaccinations['age'][i] < 25:
                    countyVaccines[vaccinations['fips'][i]]['18-24'] += 1
                elif vaccinations['age'][i] < 45:
                    countyVaccines[vaccinations['fips'][i]]['25-44'] += 1
                elif vaccinations['age'][i] < 65:
                    countyVaccines[vaccinations['fips'][i]]['45-64'] += 1
                else:
                    countyVaccines[vaccinations['fips'][i]]['65+'] += 1
            
            vaccinated = pd.DataFrame(data=countyVaccines).transpose()

            vaccinated.to_csv(cache)
            return vaccinated
        else:
            # fetch data
            gen_sample_data(file=vaccinations_file)
            fetch_vaccinations(cache=cache, vaccinations_file=vaccinations_file)

def gen_sample_data(n=10000, distribution="population", file="vaccinations.csv"):
    global wisconsin_census
    if wisconsin_census is None:
        fetch_census()

    split = {}
    runningTotal = 0

    for i in range(len(wisconsin_census['fips'])):
        split[runningTotal] = wisconsin_census['fips'][i]
        runningTotal += wisconsin_census[distribution][i]

    vaccinations = {'uuid':[], 'fips': [], 'gender': [], 'age': []}
    rn = random.randint(100000, 900000)
    for i in range(10000):
        n = random.randint(0,runningTotal-1)
        # print(n)

        fips = 0

        for k in split.keys():
            if k > n:
                break
            fips = split[k]
        # print(fips)
        vaccinations['uuid'].append((i+1)*rn%911233)
        vaccinations['fips'].append(fips)
        vaccinations['gender'].append('male' if random.random()<0.5 else 'female')
        vaccinations['age'].append(random.randint(0,80))
    vaccinated = pd.DataFrame(data=vaccinations)
    vaccinated.to_csv(file)
    return vaccinated

def wisconsin_census(property):
    values, fips = []
    for (f, v) in zip(wisconsin_census['fips'], wisconsin_census[property]):
        fips.append(f)
        values.append(v)
    return (values, fips)

def covid_cases(property):
    values, fips = []
    for (f, v) in zip(covid_cases['fips'], covid_cases[property]):
        fips.append(f)
        values.append(v)
    return (values, fips)

def vaccinated(property):
    values, fips = []
    for (f, v) in zip(vaccinated['fips'], vaccinated[property]):
        fips.append(f)
        values.append(v)
    return (values, fips)

def order(fips, values):
    ordered = []
    for f in codes:
        ordered.append(values[fips.index(f)])
    return ordered

def county_list():
    return counties

def code_list():
    return codes