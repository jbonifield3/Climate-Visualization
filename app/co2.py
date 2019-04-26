# -*- coding: utf-8 -*-
"""
CO2 load class for CSE 
project
By: D. CARVALLO
"""
import os

import pandas as pd
from constants import PATH_TO_DATA_DIR, STATE_TO_ABBR_MAP


def get_CO2(dta_type='State', year=None, url=None):
    #get the coresponding CO2 data
    #dta_type options => state or LatLong
    if dta_type == 'State':
        #get the EIA data
        #read in CO2 data and get in right format by STATE
        if url==None:
            df = pd.read_csv(os.path.join(PATH_TO_DATA_DIR, 'CO2-Data-By-Category.csv'))
        else:
            df = pd.read_csv(url)
        df['STT'] = df.State.apply(lambda x: STATE_TO_ABBR_MAP[x])
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
            df = pd.read_csv(os.path.join(PATH_TO_DATA_DIR, 'CO2-data.csv'))
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


if __name__ == '__main__':
    get_CO2()