import re

import pandas as pd
import requests

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
}
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


def get_all_states():
    dfs = []
    for state, abbr in states.items():
        temp = get_berkeley_data(state)[0]
        temp['state'] = abbr
        dfs.append(temp.reset_index())
    return pd.concat(dfs).set_index(['year', 'state']).sort_index()
