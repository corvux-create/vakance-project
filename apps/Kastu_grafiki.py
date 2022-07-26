#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


from app import app

""" df = pd.read_csv('world_countries_2.csv')

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group") """

meteoParametri = pd.read_csv('meteo_parametri.csv')

fig_kopa = px.box(meteoParametri, y=['x1', 'x2', 'x3'], title="Visas trīs stacijas")
fig_1 = px.box(meteoParametri, y='x1', title="1.stacija" )
fig_2 = px.box(meteoParametri, y='x2', title="2.stacija")
fig_3 = px.box(meteoParametri, y='x3', title="3.stacija")

row = dbc.Container(
    [
        dbc.Row(dbc.Col
            (html.H2(
                children='Kastu grafiki pirms datu koriģēšanas',
                style={
                    'textAlign': 'center',
                    'color': '#006168'
                }
                )
            )
        ),
        dbc.Row(dbc.Col
            (
                dcc.Graph(
                    id='spacy-graph',
                    figure=fig_kopa
                ),
                md=12
            ), 
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='spacy-graph',
                        figure=fig_1
                    ),
                    md=4
                ),
                dbc.Col(
                    dcc.Graph(
                        id='spacy-graph',
                        figure=fig_2
                    ),
                    md=4
                ),
                dbc.Col(
                    dcc.Graph(
                        id='spacy-graph',
                        figure=fig_3
                    ),
                    md=4
                )
            ]
        ),
    ],
    fluid=True,
)

Kastu_grafiki_layout = html.Div([row])