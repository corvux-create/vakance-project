import plotly.graph_objects as go
import requests

import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import dash_leaflet as dl


from app import app

url = 'http://api.open-notify.org/iss-now.json'
time = []
latitude = []
longitude = []


row = html.Div(
    [
        dbc.Row(dbc.Col
            (html.H2(
                children='International Space Station Current Location. Live update',
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
                        dcc.Graph(
                            style={},
                            id='live-graph-latitude', 
                            animate=False,
                        )
                    ),

                    dbc.Row(
                        dcc.Graph(
                            style={},
                            id='live-graph-longitude', 
                            animate=False,
                        )
                    )
                ]),
                dbc.Col(dl.Map([dl.TileLayer(url='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png'),
                                dl.LayerGroup(id="layer")],
                                id="map", zoom=1, center=(20.0, 30.0), style={'width': '100%', 'height': '70vh',
                                'margin': "auto", "display": "block"}),)
            ]
        ),
    ]
)

satellite_position_layout = html.Div([row, dcc.Interval(
            id='graph-update',
            interval=1*1000, # in milliseconds
        )])

''' satellite_position_layout = html.Div(
   [
        html.H2(
            children='International Space Station Current Location. Live update',
            style={
                'textAlign': 'center',
                'color': '#006168'
            }
            ),
        html.Div(children=[
                html.Div (style={'width': '49%', 'display': 'inline-block'},
                        children=[
                                dcc.Graph(style={},
                                id='live-graph-latitude', 
                                animate=False,
                                ),
                            dcc.Graph(style={},
                                        id='live-graph-longitude', 
                                        animate=False,

                                ),
                        ]
                        
                ),
                html.Div (style={'width': '49%', 'display': 'inline-block', 'float': 'right'},
                        children=[
                                dl.Map([dl.TileLayer(url='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png'), dl.LayerGroup(id="layer")],
                                        id="map", zoom=1, center=(20.0, 30.0), style={'width': '100%', 'height': '70vh',
                                        'margin': "auto", "display": "block"}),
                        ]            
                    ),
            ]
        ),
       
        dcc.Interval(
            id='graph-update',
            interval=1*1000, # in milliseconds
        )
    ]
) '''
@app.callback(Output("layer", "children"), [Input("graph-update", "n_intervals")])
def update_map(n):
    r = requests.get(url)
    # Сохранение ответа API в переменной.
    response_dict = r.json()
    lat = response_dict['iss_position']['latitude']
    lng = response_dict['iss_position']['longitude']
    return [dl.Marker(position=[lat, lng])]



@app.callback(Output('live-graph-latitude', 'figure'),

              [Input('graph-update', 'n_intervals')])


def update_graph_scatter_latitude(n):
    r = requests.get(url)
    # Сохранение ответа API в переменной.
    response_dict = r.json()
    time.append(datetime.datetime.fromtimestamp(response_dict['timestamp']).strftime('%H:%M:%S'))
    latitude.append(response_dict['iss_position']['latitude'])
    longitude.append(response_dict['iss_position']['longitude'])

    if len(time)>10:
        del time[0]
        del latitude[0]
        del longitude[0]
    
    data = go.Scatter(
            x=list(time),
            y=list(latitude),
            name='Scatter',
            mode= 'lines+markers',
            
            )

    return {'data': [data],
            'layout' : go.Layout(
                                          xaxis=dict(title_text = "time stamp"),
                                            yaxis=dict(title_text = "latitude"),  
#                                         xaxis=dict(range=[min(time), max(time)]),
#                                         yaxis=dict(range=[min(latitude), max(latitude)])
                                    )}


@app.callback(Output('live-graph-longitude', 'figure'),

              [Input('graph-update', 'n_intervals')])
def update_graph_scatter_longitude(n):
    
    data = go.Scatter(
            x=list(time),
            y=list(longitude),
            name='Scatter',
            mode= 'lines+markers',
            
            )
    

    return {'data': [data],
            'layout' : go.Layout(
                                           xaxis=dict(title_text = "time stamp"),
                                            yaxis=dict(title_text = "longitude"),
#                                         xaxis=dict(range=[min(time), max(time)]),
#                                         yaxis=dict(range=[min(longitude), max(longitude)])
                                    )}


""" if __name__ == '__main__':
    app.server.run(port=8050, host='127.0.0.1'),
    app.run_server(debug=True, use_reloader=False) """