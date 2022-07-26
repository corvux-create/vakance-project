#!/usr/bin/env python
# coding: utf-8

# In[3]:

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import Kastu_grafiki, Kastu_grafiki_pec_korigesanas

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-180259406-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'UA-180259406-1');
        </script>

        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Interactive dashboard", className="display-5"),
        html.Hr(),
        html.P(
            "Uzdevums Datu analītiķa vakancei", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Kastu grafiki pirms datu koriģēšanas", href="/", id="page-1-link"),
                dbc.NavLink("Kastu grafiki pēc koriģēšanas", href="/apps/Kastu_grafiki_pec_korigesanas", id="Kastu-grafiki-pec-korigesanas-link"),
                dbc.NavLink("Weibula sadalījums", href="/apps/Weibula sadalījums", id="Weibula-sadalijums-link"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([
        html.Div(id='page-content')
    ], style=CONTENT_STYLE
)    

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output('page-content', 'children'),
              [Input("url", "pathname")],)
def display_page(pathname):
    if pathname == '/':
        return Kastu_grafiki.Kastu_grafiki_layout
    if pathname == '/apps/Kastu_grafiki_pec_korigesanas':
        return Kastu_grafiki_pec_korigesanas.Kastu_grafiki_pec_korigesanas_layout
    if pathname == '/apps/Weibula_sadalijums':
        return Weibula_sadalijums.Weibula_sadalijums_layout
    if pathname == '/apps/satellite_position':
        return satellite_position.satellite_position_layout
    elif pathname == '/apps/World_countries':
        return World_countries.World_countries_layout
    elif pathname == '/apps/Named_Entity_Recognition':
        return Named_Entity_Recognition.Named_Entity_Recognition_layout
    else:
        return '404'

if __name__ == '__main__':
    app.server.run(port=8080, host='127.0.0.1'),
    app.run_server(debug=True)

