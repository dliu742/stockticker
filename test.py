import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
import plotly.graph_objects as go
import dash_daq as daq

# set dash plotly figures
app = dash.Dash(external_stylesheets=[dbc.themes.GRID])

fig = go.Figure()

button_group = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.RadioItems(
                        id="play",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Pause", "value": 'Pause'},
                            {"label": "Play", "value": 'Play'},
                        ],
                        value='Play',
                    ), width=5, align='right'
                ),
                dbc.Col(
                    dbc.RadioItems(
                        id="crypto",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Crypto", "value": 'Crypto'},
                            {"label": "All Stocks", "value": 'All Stocks'},
                        ],
                        value='All Stocks',
                    ), width=5
                ),
                dbc.Col(
                    dbc.Button(
                        children="Next",
                        color="dark",
                        className="me-1"
                    ), width=2
                )
            ]
        ),
        html.Div(id="output")
    ],
    className="radio-group",
)

text_group = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(children='Jan-07, 2023',
                            id='date',
                            style={'color': 'white',
                                   'fontSize': 80,
                                   'text-align': 'center',
                                   'padding': 0,
                                   'margin': 0})
                ),
                dbc.Col(
                    html.H1(children='10:55AM',
                            id='current_time',
                            style={'color': 'white',
                                   'fontSize': 80,
                                   'text-align': 'center',
                                   'padding': 0,
                                   'margin': 0})
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.P(children='Ticker: ',
                          id='ticker_text',
                          style={'color': 'white',
                                 'fontSize': 40,
                                 'text-align': 'center',
                                 'padding': 0}),
                    width=2
                ),
                dbc.Col(
                    html.P(children='AMD',
                           id='ticker_name',
                           style={'color': 'white',
                                  'fontSize': 40,
                                  'text-align': 'left',
                                  'padding': 0}),
                    width=2
                ),
                dbc.Col(
                    html.P(children='$63.96',
                           id='ticker_price',
                           style={'color': 'white',
                                  'fontSize': 40,
                                  'text-align': 'center',
                                  'padding': 0}),
                    width=5
                ),
                dbc.Col(
                    html.P(children='$1.63 (2.35%)',
                           id='ticker_price_change',
                           style={'color': 'white',
                                  'fontSize': 40,
                                  'text-align': 'center',
                                  'margin': 0}),
                    width=3
                )

            ]
        )
    ]
)


graph_group = html.Div(
    [
        dcc.Graph(figure=fig, id='graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ]
)


radio_group = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    daq.BooleanSwitch(on=True,
                                      label='Play',
                                      id='btn-play',
                                      labelPosition="top",
                                      style={'color': 'white',
                                             'fontSize': 12,
                                             'text-align': 'left',
                                             'padding': 0,
                                             'margin': 0}
                                  )
                ),
                dbc.Col(
                    daq.BooleanSwitch(on=False,
                                      label='Crypto Only',
                                      id='btn-crypto',
                                      labelPosition="top",
                                      style={'color': 'white',
                                             'fontSize': 12,
                                             'text-align': 'left',
                                             'padding': 0,
                                             'margin': 0}
                                  )
                )
            ]
        ),
        dbc.Row(html.Div('test', id='testing'))
    ]
)


app.layout = html.Div([text_group, graph_group, button_group], style={'backgroundColor': 'black'})


@app.callback(Output("output", "children"), [Input("play", "value")])
def display_value(value):
    return f"Selected value: {value}"


# main function for the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
