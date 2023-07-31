import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import sys
import os

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

logo_2 = "http://www2.decom.ufop.br/terralab/wp-content/uploads/2020/07/terraLabLogo-Horizontal-228x45.png"


logo = app.get_asset_url("logo1.png")
logo = './' + logo

print(logo)

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
                html.Div(id=logo, style={
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
                )
            ]),
            dbc.Col(style=header_col_style, children=[
                html.Div("Fim: ", style=text_label_style),
                dcc.DatePickerSingle(
                    id="end-date-picker",
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
                                    }
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.run_server(debug=True)
    else:
        app.run_server(debug=True)