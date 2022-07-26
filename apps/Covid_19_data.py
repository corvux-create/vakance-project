#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import dash_leaflet as dl

from app import app

# new code
url = 'https://api.covid19api.com/summary'
r = requests.get(url, verify=False)
# Сохранение ответа API в переменной.
response_dict = r.json()

# Анализ информации о репозиториях.
repo_dicts = response_dict['Countries']

Country, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered,TotalRecovered, Slug = ([],[], [], [], [], [], [], [])

for repo_dict in repo_dicts:
    Country.append(repo_dict['Country'])
    NewConfirmed.append(repo_dict['NewConfirmed'])
    TotalConfirmed.append(repo_dict['TotalConfirmed'])
    NewDeaths.append(repo_dict['NewDeaths'])
    TotalDeaths.append(repo_dict['TotalDeaths'])
    NewRecovered.append(repo_dict['NewRecovered'])
    TotalRecovered.append(repo_dict['TotalRecovered'])
    Slug.append(repo_dict['Slug'])

df = pd.read_csv('countru_coord.csv')

# To avoid "arrays must all be same length" error

a = {"Country": Country,
    "NewConfirmed": NewConfirmed,
    "TotalConfirmed": TotalConfirmed, 
    "NewDeaths": NewDeaths, 
    "TotalDeaths": TotalDeaths,
    "NewRecovered": NewRecovered,
    "TotalRecovered": TotalRecovered,
    "Slug": Slug
}

df_2 = pd.DataFrame.from_dict(a, orient='index')
df_2 = df_2.T

# Drop "Country" column from df_2 dataframe
df_3 = df_2.drop(['Country'], axis=1)

# Merge df and df_3 dataframes
df_5 = pd.merge(df_3, df, on=['Slug'])

# getting data for the first map
markers = [dl.Marker(children=dl.Tooltip([html.Div(row["Country"]), html.Span(' Total cases: '), html.Span(row["TotalConfirmed"])], className= 'myCSSClass'), position=[row["Lat"], row["Lon"]],
                     draggable=True,
                     icon={"iconUrl": "/assets/marker_green_2.png", "iconSize": [20, 20]}
                    ) for i, row in df_5.iterrows()]

markers_group = dl.LayerGroup(id="markers", children=markers)


# getting data for graph

url_graph = 'https://api.covid19api.com/summary'

row = html.Div(
    [
        dbc.Row(dbc.Col
            (html.H2(
                children='Covid-19 data (source: https://api.covid19api.com)',
                style={
                    'textAlign': 'center',
                    'color': '#006168'
                }
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row(
                        html.Div(children='Choose the country:',
                            className='dash-component-label'       
                        )
                    ),
                    dbc.Row(
                        dcc.Dropdown(
                            id='cases-dropdown-by-day',
                            options=[{'label': i, 'value': j} for i, j in zip(df_2['Country'], df_2['Slug'])],
                            value='latvia',
                            style={'width': '100%'}
                        ),
                    ),

                    dbc.Row(
                        dcc.Graph(style={'width': '100%', 'display': 'inline-block'},
                            id='cases-covid-by-day',
                        ),
                    )
                ]),
                dbc.Col(dl.Map([dl.TileLayer(url='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png'), markers_group], zoom=3,
                                        style={'width': '100%',
                                                  'display': 'inline-block',
                                                  'height': '500px'},
                         id='example-graph-map',
                        
                    )
                )
            ]
        ),
      
            dash_table.DataTable(
                id='datatable-paging',
                data=df_2.to_dict('records'),
                sort_action='native',
                # columns=[{'id': c, 'name': c} for c in df_2.columns],
                columns=[{"name": "Country", "id": "Country"},
                        {"name": "Total confirmed cases", "id": "TotalConfirmed"},
                        {"name": "Total deaths", "id": "TotalDeaths"},
                        {"name": "Total recovered", "id": "TotalRecovered"},
                        ],
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Country'},
                        'textAlign': 'left'
                    }
                ],
                style_cell={
                    'fontFamily': 'Ubuntu',
                    'textAlign': 'center',
                    'fontSize': '18px',
    #                 'backgroundColor': 'rgb(50, 50, 50)',
    #                 'color': 'white'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontFamily': 'Ubuntu',
                    'fontSize': '20px',
                    'fontColor': 'red',
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                },       
            ),
      

    ]
)

Covid_19_data_layout = html.Div([row])


# world new cases by day
@app.callback(
    Output('cases-covid-by-day', 'figure'),
    [Input('cases-dropdown-by-day', 'value')])
def update_figure(value):
    
    url_graph = 'https://api.covid19api.com/total/dayone/country/'+value
    r_graph = requests.get(url_graph, verify=False)
    response_dict_graph = r_graph.json()
    
    Confirmed, Deaths, Date = [], [], []

    for response_dicts_graph in response_dict_graph:
        Confirmed.append(response_dicts_graph['Confirmed'])
        Deaths.append(response_dicts_graph['Deaths'])
        Date.append(response_dicts_graph['Date'])
      
    df_4 = pd.DataFrame(data={"Time stamp": Date,
                              "Confirmed": Confirmed,
                              "Deaths": Deaths,
                              })

    fig = px.scatter(df_4, x="Time stamp", y=["Confirmed", "Deaths"]
                    #  size="pop", color="continent", hover_name="country", 
                     )
#    
    fig.update_layout(transition_duration=500,
                     paper_bgcolor='#cfe0d8',
                     plot_bgcolor='#f3dbb3',
                     yaxis_gridcolor='#e03460'
                     )
    fig.update_xaxes(tickfont=dict(family='Rockwell', color='green', size=14), title_font=dict(size=24, family='cursive', color='crimson'))
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='blue', size=16), title_font=dict(size=24, family='cursive', color='crimson'))
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig
