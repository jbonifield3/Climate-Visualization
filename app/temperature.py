import os
import re

import pandas as pd
import requests

from constants import PATH_TO_DATA_DIR, STATE_TO_ABBR_MAP


input_columns = [
    'year',
    'month',
    '1m',
    '1m_unc',
    '1y',
    '1y_unc',
    '5y',
    '5y_unc',
    '10y',
    '10y_unc',
    '20y',
    '20y_unc'
]


keep_columns = [
    'year',
    'month',
    '1y',
    '5y',
    '10y',
    '20y',
]

def load_temperature_data():
    cache_file = os.path.join(PATH_TO_DATA_DIR, 'temperature.csv')

    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        dfs = []
        for state, abbr in STATE_TO_ABBR_MAP.items():
            temp = get_berkeley_data(state)[0]
            temp['state'] = abbr
            dfs.append(temp.reset_index())

        df = pd.concat(dfs)
        df.to_csv(cache_file)

    return df.set_index(['year', 'state']).sort_index()


def get_temperature_min_and_max(df):
    df_min = df.min()
    df_max = df.max()
    mins = {}
    maxes = {}
    for avg_window in ('1y', '5y', '10y', '20y'):
        mins[avg_window] = df_min[avg_window]
        maxes[avg_window] = df_max[avg_window]
    return mins, maxes


def get_berkeley_metadata(uri):
    absolute_temp = None
    skiprows = 0
    temp_re = re.compile(r'% Estimated Jan 1951-Dec 1980 absolute temperature \(C\): ([-]?\d+\.\d+)')
    with requests.get(uri) as r:
        for line in r.text.split('\n'):
            skiprows += 1
            if not line.startswith('%'): break
            if not absolute_temp:
                match = re.match(temp_re, line)
                if match:
                    absolute_temp = float(match.group(1))
    return absolute_temp, skiprows


def get_berkeley_data(state):
    state = state.lower().replace(' ', '-')
    uri = 'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/{}-TAVG-Trend.txt'.format(state)
    absolute_temp, skiprows = get_berkeley_metadata(uri)
    df = pd.read_csv(
        uri,
        sep=r'\s+',
        skiprows=skiprows,
        names=input_columns,
        usecols=keep_columns,
        index_col=['year', 'month']
    )
    relative = df.xs(6, level='month')
    absolute = relative + absolute_temp
    return relative, absolute


if __name__ == '__main__':
    load_temperature_data()