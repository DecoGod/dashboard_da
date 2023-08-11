import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
import sys
import os
from functions import *

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

logo_2 = "http://www2.decom.ufop.br/terralab/wp-content/uploads/2020/07/terraLabLogo-Horizontal-228x45.png"


# logo = app.get_asset_url("logo1.png")
# logo = './' + logo

# print(logo)

data_inicial = "2023-02-01"
data_final   = "2023-02-28"
success = get_successful_geocode(data_inicial, data_final)
fails = get_fails_geocode(data_inicial, data_final)
fig1 = graph_hit_fails(success,fails)

background_style = {
    "height": "100vh",
    "background-color": "#242424",
    "margin": "0",
    "padding": "0",
}

header_style = {
    "height": "139px",
    "width": "100vw",
    "border-bottom": "1px solid #404040",
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
}

header_col_style = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
}

text_label_style = {
    "color": "#AAAAAA",
    "padding-right": "15px",
}

app.layout = html.Div(
    [
        html.Div(id="header", style=header_style, children=[
            dbc.Col(
                html.Div(id=logo_2, style={
                    "display": "flex",
                    "justify-content": "center"
                }, children=[
                    html.Img(src=logo_2, style={
                        "height": "53px",
                        "width": "227px"
                    })
                ])
            ),
            dbc.Col(
                html.Div(
                    "Geocodificações",
                    style={
                        "color": "#AAAAAA",
                        "font-size": "35px",
                        "display": "flex",
                        "justify-content": "center"
                    })
            ),
            dbc.Col(style=header_col_style, children=[
                html.Div("Inicio: ", style=text_label_style),
                dcc.DatePickerSingle(
                    id="start-date-picker",
                    date="2023-02-01"
                )
            ]),
            dbc.Col(style=header_col_style, children=[
                html.Div("Fim: ", style=text_label_style),
                dcc.DatePickerSingle(
                    id="end-date-picker",
                    date="2023-02-28"
                )
            ]),
            dbc.Col(style=header_col_style, children=[
                html.Div("Dashboard: ", style=text_label_style),
                dcc.Dropdown(
                    style={
                        "width": "160px",
                        # "height": "48px",
                    },
                    options=[
                        {'label': 'Dashboard 1', 'value': '1'},
                        {'label': 'Dashboard 2', 'value': '2'},
                        {'label': 'Dashboard 3', 'value': '3'},
                        {'label': 'Dashboard 4', 'value': '4'}
                    ],
                    value='1'
                )
            ])
        ]),       
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(style={
                            "padding" : "0px"
                            },
                            children = [
                                html.Div(
                                    style={
                                        "background-color": "#2E2E2E",
                                        "height": "600px",
                                        "width": "800px",
                                        "margin-right" : "10px"
                                    }
                                )
                            ]
                        ),
                        dbc.Col(style={
                            "padding" : "0px"
                            },
                            children = [
                                html.Div(
                                    style={
                                        "background-color": "#2E2E2E",
                                        "height": "295px",
                                        "width": "800px",
                                        "margin-bottom" : "10px"
                                    },
                                    children= [
                                        dcc.Graph(
                                            id = "Figure1",
                                            figure= fig1
                                        )
                                    ]
                                ),
                                html.Div(
                                    style={
                                        "background-color": "#2E2E2E",
                                        "height": "295px",
                                        "width": "800px",
                                    }
                                ),
                            ]
                        ),
                    ],
                    justify="center",
                )
            ],
            style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "calc(100vh - 139px)"},
        ),
    ],
    style=background_style
)
server = app.server

@callback(
    [
        Output('Figure1','figure')
    ],
    [
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date')
    ]
)
def update_start_date(start,end):
    success = get_successful_geocode(start, end)
    fails = get_fails_geocode(start, end)
    fig1 = graph_hit_fails(success,fails)
    return [fig1]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.run_server(debug=True)
    else:
        app.run_server(debug=True)

