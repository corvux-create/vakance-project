#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import json

import dash_leaflet as dl
from dash_leaflet import express as dlx

from app import app

df = pd.read_csv('world_countries_2.csv')

# getting data for first map
with open("country_new.json", encoding='utf-8') as world_countries:
    val = world_countries.read()
    marker_data=json.loads(val)
    

# markers = [dl.Marker(children=dl.Tooltip(row["name"] + " population: " + str(row["population"]), className= 'myCSSClass'), position=[row["latlng"][0], row["latlng"][1]],
#                      draggable=True,
#                      icon={"iconUrl": "/assets/marker_green.png", "iconSize": [30, 30]}
#                      ) for i, row in df.iterrows()]

markers = [dl.Marker(children=dl.Tooltip([html.Div(item["name"]), html.Span("capital: "), html.Span(item["capital"])], className= 'myCSSClass'), position=item["latlng"],
                     draggable=True,
                     icon={"iconUrl": "/assets/marker_green.png", "iconSize": [30, 30]}
                    ) for item in marker_data]

markers_group = dl.LayerGroup(id="markers", children=markers)


World_countries_layout = html.Div(style={},
    children=[
    html.H2(style={'textAlign': 'center', 'color': '#006168'},
            children='World countries'),
        
        html.Div(style={},
             children=[   
                    html.Div(children='Choose the region:',
                        className='dash-component-label'       
                    ),                   
                    dcc.Dropdown(
                        style={'width': 300,
                              'backgroundColor': '#4CAF50',
                              'fontSize': 20
                        },
                        id='demo-dropdown',
                        options=[{'label': i, 'value': i} for i in df['region'].unique()],
                        value='Europe'
                    ),
                     dcc.Graph(id='graph-with-dropdown'),
                                  
                    dl.Map([dl.TileLayer(), markers_group], zoom=3, style={'width': '100%',

                                                  'display': 'inline-block',
                                                  'height': '600px'},
                         id='example-graph-map',
                        
                    ),
             ]
        ),
           
])

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('demo-dropdown', 'value')])
def update_figure(selected_region):
    filtered_df = df[df.region == selected_region]

    fig = px.bar(filtered_df, x="name", y="population", text='population', color='population',
                        labels={
                             "name": "country"
                         },
                     )
#    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(transition_duration=500,
                     paper_bgcolor='#cfe0d8',
                     plot_bgcolor='#f3dbb3',
                     yaxis_gridcolor='#e03460',
                      font_size=12,
                      uniformtext_minsize=12,
                      uniformtext_mode='show',
                     )
    
#     fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    fig.update_xaxes(tickfont=dict(family='Rockwell', color='green', size=14), title_font=dict(size=24, family='Courier', color='#944f11'))
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='blue', size=16), title_font=dict(size=24, family='Courier', color='#944f11'))
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig


# if __name__ == '__main__':
#     app.server.run(port=8000, host='127.0.0.1'),
#     app.run_server(debug=True, use_reloader=False)

