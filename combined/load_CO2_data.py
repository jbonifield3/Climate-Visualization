# -*- coding: utf-8 -*-
"""
CO2 load class for CSE 
project
By: D. CARVALLO
"""
import pandas as pd
states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'United States': 'USA',
    'District of Columbia': 'DC',
}


def get_CO2(dta_type='State', year=None, url=None):
    #get the coresponding CO2 data
    #dta_type options => state or LatLong
    if dta_type == 'State':
        #get the EIA data
        #read in CO2 data and get in right format by STATE
        if url==None:
            df = pd.read_csv("CO2-Data-By-Category.csv")
        else:
            df = pd.read_csv(url)
        df['STT'] = df.State.apply(lambda x: states[x])
        #Filter to get the states only
        df = df[df.STT != 'USA']
        df = df[df.STT != 'DC']
        
        if year == None:
            return df
        else: 
            data = df[['State', 'STT', str(year), 'Percent', 'Absolute', 'category']]
            return data
        
    elif dta_type == 'LatLong':
        if url == None:
            df = pd.read_csv('CO2-data.csv')
        else:
            df = pd.read_csv(url)
        # Set longitude to (-180, +180]
        df['DLONG'] = df['LONG'] - 180
        # Set longitude to [-90, +90)
        df['DLAT'] = -df['LAT'] + 90
        
        if year == None:
            return df
        else: 
            data = df[['DLAT', 'DLONG', str(year)]]
            return data 
    else:
        return IndexError

