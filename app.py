# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import flask

from temperature import load_temperature_data, get_temperature_min_and_max
from co2 import get_CO2
from power import load_power_data


external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

#Check if data directory exists and if not create it
if not os.path.exists('data'):
    os.makedirs('data')

# Load & process datasets
temp_df = load_temperature_data()

co2_df = get_CO2(dta_type='State') #Load in all the state information
co2_df = co2_df.groupby(['STT']).sum().reset_index() #group by the state

power_df = load_power_data()

# Calculate constants
MIN_TEMPS, MAX_TEMPS = get_temperature_min_and_max(temp_df)
MAX_CO2 = co2_df.loc[:, co2_df.columns != 'STT'].max().max()
MIN_CO2 = 0

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

START_YEAR = 1980
END_YEAR = 2013

app.layout = html.Div(children=[
    html.Div(
        className='row col-xs-12',
        children=[
            html.H3('Visualizing Long-Term Trends in US Power Generation, CO2 Emissions, and Surface Temperature')
        ],
    ),

    html.Div(
        className="row",
        children=[
            html.Div(
                className='col-xs-3',
                children=[
                    html.Br(),
                    html.Label('Select data to display:'),
                    dcc.Checklist(
                        id="select-data",
                        values=['temp', 'power']
                    ),
                    html.Br(),
                    html.Label('Filter selected data:'),
                    html.Div(
                        id="data-filters",
                        children=[
                            html.Div(
                                id='temperature-filters',
                                children=[
                                    html.Label(
                                        'Temperature averaging window'
                                    ),
                                    dcc.RadioItems(
                                        id='temp-avg-window',
                                        options=[
                                            {'label': '1-year', 'value': '1y'},
                                            {'label': '5-year', 'value': '5y'},
                                            {'label': '10-year', 'value': '10y'},
                                            {'label': '20-year', 'value': '20y'},
                                        ],
                                        value='10y'
                                    )
                                ],
                                style={'marginTop': '5px'}
                            ),
                            html.Div(
                                id='power-filters',
                                children=[
                                    html.Label(
                                        'Power generation class'
                                    ),
                                    dcc.RadioItems(
                                        id='power-class',
                                        options=[
                                            {'label': 'All', 'value': 'All'},
                                            {'label': 'Clean', 'value': 'Clean'},
                                            {'label': 'Fossil', 'value': 'Fossil'},
                                        ],
                                        value='All'
                                    )
                                ],
                                style={'marginTop': '5px'}
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className='col-xs-9',
                children=[
                    dcc.Graph(id='main-graph'),
                ]
            )
        ]
    ),
    html.Label('Select year:'),
    html.Div(
        style={'height': '50px'},
        children=[
            dcc.Slider(
                id="select-year",
                min=START_YEAR,
                max=END_YEAR,
                marks={i: str(i) for i in range(START_YEAR, END_YEAR + 1, 5)},
                value=START_YEAR
            )
        ]
    )
])


@app.callback(
    Output(component_id='select-data', component_property='options'),
    [Input(component_id='select-data', component_property='values')]
)
def update_data_checklist(values):
    options = [
        {'label': 'Temperature Anomaly', 'value': 'temp'},
        {'label': 'CO2 Emissions', 'value': 'co2'},
        {'label': 'Power Generation', 'value': 'power'},
    ]
    if 'temp' in values:
        options[1]['disabled'] = True
    elif 'co2' in values:
        options[0]['disabled'] = True

    return options


@app.callback(
    Output(component_id='temperature-filters', component_property='className'),
    [Input(component_id='select-data', component_property='values')]
)
def display_temperature_filters(data_selection):
    return None if 'temp' in data_selection else 'hidden'


@app.callback(
    Output(component_id='power-filters', component_property='className'),
    [Input(component_id='select-data', component_property='values')]
)
def display_power_filters(data_selection):
    return None if 'power' in data_selection else 'hidden'


@app.callback(
    Output(component_id='main-graph', component_property='figure'),
    [
        Input(component_id='select-data', component_property='values'),
        Input(component_id='select-year', component_property='value'),
        Input(component_id='temp-avg-window', component_property='value'),
        Input(component_id='power-class', component_property='value'),
    ]
)
def update_figure(data_selection, year, temp_avg_window, power_class):
    visibility = [
        True if data_series in data_selection else False
        for data_series in ['temp', 'co2', 'power']
    ]

    temp_df_yr = temp_df.xs(year, level='year')
    power_df_yr = power_df[power_df['year'] == year]
    if power_class in ('Clean', 'Fossil'):
        power_df_yr = power_df_yr[power_df_yr['Class'] == power_class]

    return {
        'data': [
            go.Choropleth(
                visible=visibility[0],
                name='Temperature',
                locations=temp_df_yr.reset_index()['state'],
                text=temp_df_yr[temp_avg_window].apply(lambda x: '%.2f °C' % x),
                hoverinfo='location+text+name',
                z=temp_df_yr[temp_avg_window],
                zmin=MIN_TEMPS[temp_avg_window],
                zmid=0,
                zmax=MAX_TEMPS[temp_avg_window],
                locationmode='USA-states',
                colorscale='RdBu',
                colorbar=dict(
                    title='Temperature',
                    ticksuffix=' ° C',
                    showticksuffix='last',
                    len=0.8
                )
            ),
            go.Choropleth(
                visible=visibility[1],
                name='CO2',
                locations=co2_df['STT'],
                text=co2_df[str(year)].apply(lambda x: '{:,.2f} KG CO2'.format(x)),
                hoverinfo='location+text+name',
                z=co2_df[str(year)],
                zmin=MIN_CO2,
                zmax=MAX_CO2,
                locationmode='USA-states',
                colorscale='Greys',
                reversescale=True,
                colorbar=dict(
                    title='CO<sub>2</sub>',
                    ticksuffix=' KG',
                    showticksuffix='last',
                    len=0.8
                )
            ),
            go.Scattergeo(
                visible=visibility[2],
                name='Power',
                locationmode='USA-states',
                lat=power_df_yr['Latitude'],
                lon=power_df_yr['Longitude'],
                mode='markers',
                marker=go.scattergeo.Marker(
                    size=power_df_yr['size'],
                    color=power_df_yr['color'],
                    opacity=0.7,
                    line=dict(
                        color='rgb(51,51,51)',
                        width=1
                    )
                ),
                text=power_df_yr[['plant name', 'netgen']].apply(
                    lambda x: '{}<br>Net Generation (MWh): {:,.0f}'.format(x[0], x[1]),
                    axis=1
                ),
                hoverinfo='text+name'
            )
        ],
        'layout': go.Layout(
            title = go.layout.Title(
                text = 'Display year: %i' % year
            ),
            height=600,
            geo=go.layout.Geo(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            )
        )
    }


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
