import os

import pandas as pd

from constants import PATH_TO_DATA_DIR, MIN_MARKER_SIZE, MAX_MARKER_SIZE


def load_power_data(force_update=False):
    cache_file = os.path.join(PATH_TO_DATA_DIR, 'power.csv')
    if not force_update and os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        df = pd.read_csv('https://docs.google.com/spreadsheets/d/1Pn3L_yltqpL92LQ-pxy8GwiXDaaxbsKELlM_Yrv3v_4/export?format=csv')
        max_netgen = df['netgen'].max()
        min_netgen = df['netgen'].min()
        def get_size(row_entry):
            return MIN_MARKER_SIZE + \
                   ((row_entry['netgen'] - min_netgen) / (max_netgen - min_netgen)) * \
                   (MAX_MARKER_SIZE - MIN_MARKER_SIZE)
        df['color'] = df.apply(get_color, axis=1)
        df['size'] = df.apply(get_size, axis=1)
        df.to_csv(cache_file)
    return df


def get_color(row_entry):
    if row_entry['Class'] == 'Clean':
        return 'rgb(0, 128, 0)'
    elif row_entry['Class'] == 'Fossil':
        return 'rgb(255, 0, 0)'


if __name__ == '__main__':
    load_power_data(force_update=True)
