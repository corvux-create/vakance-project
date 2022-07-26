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

import spacy
# from spacy.displacy.render import DEFAULT_LABEL_COLORS
from collections import Counter

from app import app

DEFAULT_LABEL_COLORS = {
    "ORG": "#7aecec",
    "FAC": "#feca74",
    "PRODUCT": "#bfeeb7",
    "GPE": "#feca74",
    "LOC": "#ff9561",
    "PERSON": "#aa9cfc",
    "NORP": "#c887fb",
    "FACILITY": "#9cc9cc",
    "EVENT": "#FFFF00",
    "LAW": "#ff8197",
    "LANGUAGE": "#ff8197",
    "WORK_OF_ART": "#FF1493",
    "DATE": "#c4dff3",
    "TIME": "#bfe1d9",
    "MONEY": "#e4e7d2",
    "QUANTITY": "#e4e7d2",
    "ORDINAL": "#D2691E",
    "CARDINAL": "#00FF00",
    "PERCENT": "#006400",
}

with open('spacy_text.txt', encoding="utf8") as f:
    contents = f.read()

row = dbc.Container(
    [
        dbc.Row(dbc.Col
            (html.H2(
                children='Named Entity Recognition App (spaCy)',
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
                        html.Div(children='Insert your own text (English only, the maximum number of characters: 50000):',
                            className='dash-component-label',
                            style={
                              'fontSize': 20,
                              'color': 'red',
                                'textAlign': 'center',
                                'fontWeight': 'bold'
                            }       
                        )
                    ),

                    dbc.Row(
                        dcc.Textarea(
                            id='textarea-state-example',
                            value=contents,
                            maxLength=50000,
                            style={'width': '100%', 'height': 200},
                        ),
                    ),

                    dbc.Row(
                        html.Button('Run Model', id='textarea-state-example-button', n_clicks=0),
                    ),

                    
                        dcc.Graph(
                            id='spacy-graph',
                        ),
                    
                ], md=6),
                dbc.Col(
                        html.Div(
                            id='spacy-output',
                            style={'line-height': '250%', 'max-height': '700px', 'overflow-y': 'scroll'}
                        ),
                    md=6
                )
            ]
        ),
    ],
    fluid=True,
)

Named_Entity_Recognition_layout = html.Div([row])

@app.callback(
    Output('spacy-output', 'children'),
    Output('spacy-graph', 'figure'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    def entname(name):
        return html.Span(name, style={
            "font-size": "0.8em",
            "font-weight": "bold",
            "background": "#ffffff",
            "line-height": "1",
            "border-radius": "0.35em",
            "text-transform": "uppercase",
            "vertical-align": "middle",
            "margin-left": "0.5rem"
        })


    def entbox(children, color):
        return html.Mark(children, style={
            "background": color,
            "padding": "0.45em 0.6em",
            "margin": "0 0.25em",
            "line-height": "1",
            "border-radius": "0.35em",
        })


    def entity(children, name):
        if type(children) is str:
            children = [children]

        children.append(entname(name))
        color = DEFAULT_LABEL_COLORS[name]
        return entbox(children, color)


    def render(doc):
        children = []
        last_idx = 0
        for ent in doc.ents:
            children.append(doc.text[last_idx:ent.start_char])
            children.append(
                entity(doc.text[ent.start_char:ent.end_char], ent.label_))
            last_idx = ent.end_char
        children.append(doc.text[last_idx:])
        return children

    text = str(value)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    label = []
    for ent in doc.ents:
        label.append(ent.label_)

    dictionary = Counter(label)
    df = pd.DataFrame.from_dict(dictionary, orient='index')

    df = df.rename_axis('index1').reset_index()

    # adding column name to the respective columns
    df.columns = ['Label', 'Count']

    # building bar graph
    fig = px.bar(df, x='Label', y='Count', text='Count',
                        labels={
                            "Label": "Named entities"
                        },
                        color='Label',
                        color_discrete_map=DEFAULT_LABEL_COLORS
                        
                    )
    fig.update_traces(textposition='outside')

    return render(doc), fig