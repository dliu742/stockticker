import dash
import pandas
import pytz
from dash import dcc, html, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timezone

# obtain ticker from csv file
ticker_csv_file_name = 'ticker.csv'
df_ticker = pandas.read_csv(filepath_or_buffer=ticker_csv_file_name)
tech = df_ticker['tech'].dropna().tolist()
crypto = df_ticker['crypto'].dropna().tolist()
indices = df_ticker['indices'].dropna().tolist()
financials = df_ticker['financials'].dropna().tolist()
industrial = df_ticker['industrial'].dropna().tolist()
travel = df_ticker['travel'].dropna().tolist()
consumers = df_ticker['consumers'].dropna().tolist()
china = df_ticker['china'].dropna().tolist()
international = df_ticker['international'].dropna().tolist()

# selected ticket by default includes all tickers
all_tickers = indices + tech + financials + industrial + travel + consumers + china + international + crypto
selected_ticker = all_tickers
current_ticker = 0
btn_previous_clicks = 0

fig = go.Figure()

# set css file
external_stylesheets = ['/assets/page_format.css']

# set dash plotly figures
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

text_group = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(children='Jan-07, 2023',
                            id='date',
                            style={'color': 'white',
                                   'fontSize': 70,
                                   'text-align': 'center',
                                   'padding': 0,
                                   'margin': 0})
                ),
                dbc.Col(
                    html.H1(children='10:55AM',
                            id='current_time',
                            style={'color': 'white',
                                   'fontSize': 70,
                                   'text-align': 'center',
                                   'padding': 0,
                                   'margin': 0})
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.P(children='Ticker Name ',
                           id='ticker_text',
                           style={'color': 'white',
                                  'fontSize': 32,
                                  'text-align': 'center',
                                  'padding': 0}),
                    width=6
                ),
                dbc.Col(
                    html.P(children='$63.96',
                           id='ticker_price',
                           style={'color': 'white',
                                  'fontSize': 35,
                                  'text-align': 'center',
                                  'padding': 0}),
                    width=2
                ),
                dbc.Col(
                    html.P(children='$1.63 (2.35%)',
                           id='ticker_price_change',
                           style={'color': 'white',
                                  'fontSize': 35,
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

button_group = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.RadioItems(
                        id="btn-play",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Pause", "value": False},
                            {"label": "Play", "value": True},
                        ],
                        value=True,
                    ), width=2, align='right'
                ),
                dbc.Col(
                    dbc.Checklist(
                        id="checklist-input",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Index", "value": 1},
                            {"label": "Tech", "value": 2},
                            {"label": "Financials", "value": 3},
                            {"label": "Industrial", "value": 4},
                            {"label": "Travel", "value": 5},
                            {"label": "Consumers", "value": 6},
                            {"label": "Crypto", "value": 7},
                            {"label": "China", "value": 8},
                            {"label": "International", "value": 9},
                        ],
                        value=[1],
                    ), width=8
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            children="Previous",
                            color="dark",
                            className="me-1",
                            id='btn-previous'
                        ),
                        dbc.Button(
                            children="Next",
                            color="dark",
                            className="me-1",
                            id='btn-next'
                        )
                    ], width=2
                )
            ]
        ),
        html.Div(id="testing")
    ],
    className="radio-group",
)

# app layout for the dashboard
app.layout = html.Div([text_group, graph_group, button_group], style={'backgroundColor': 'black'})


# Disable or enable the interval to pause or play the auto refresh
@app.callback([Output('interval-component', 'disabled')],
              [Input('btn-play', 'value')])
def update_global_var(on):
    if on is True:
        print('interval - disable set to False')
        return [False]
    else:
        print('interval - disable set to True')
        return [True]


# update selected ticker list to be crypto or all tickers
@app.callback([Output('testing', 'children')],
              [Input('checklist-input', 'value')])
def update_global_var(checklist):
    global selected_ticker
    global current_ticker
    global all_tickers
    global crypto
    global tech
    global indices
    global financials
    global industrial
    global travel
    global consumers
    global china
    global international

    # select tickers based on user checkbox input, add it to the ticker_list array
    ticker_list = []
    current_ticker = 0
    if 1 in checklist:
        ticker_list = ticker_list + indices
        print('Indices selected')
    if 2 in checklist:
        ticker_list = ticker_list + tech
        print('Tech selected')
    if 3 in checklist:
        ticker_list = ticker_list + financials
        print('Financials selected')
    if 4 in checklist:
        ticker_list = ticker_list + industrial
        print('Industrial selected')
    if 5 in checklist:
        ticker_list = ticker_list + travel
        print('Travel selected')
    if 6 in checklist:
        ticker_list = ticker_list + consumers
        print('Consumers selected')
    if 7 in checklist:
        ticker_list = ticker_list + crypto
        print('Crypto selected')
    if 8 in checklist:
        ticker_list = ticker_list + china
        print('China selected')
    if 9 in checklist:
        ticker_list = ticker_list + international
        print('International selected')
    selected_ticker = ticker_list
    return ['customized tickers selected']


# Multiple components can update everytime interval gets fired.
@app.callback([Output('graph', 'figure'),
               Output('date', 'children'),
               Output('current_time', 'children'),
               Output('ticker_text', 'children'),
               Output('ticker_text', 'style'),
               Output('ticker_price', 'children'),
               Output('ticker_price_change', 'children'),
               Output('ticker_price_change', 'style')],
              [Input('interval-component', 'n_intervals'),
               Input('btn-next', 'n_clicks'),
               Input('btn-previous', 'n_clicks')])
def update_graph(n, btn_next, btn_previous):
    # obtain current loop and tickers
    global current_ticker
    global selected_ticker
    global crypto

    # if the previous button is pressed, decrement the current ticker by 2, if not loop to the end of the array
    if 'btn-previous' == ctx.triggered_id:
        current_ticker = current_ticker - 2
        if current_ticker == -1:
            current_ticker = len(selected_ticker) - 1
        elif current_ticker <= -2:
            current_ticker = len(selected_ticker) - 2
        symbol = selected_ticker[current_ticker]
    else:
        symbol = selected_ticker[current_ticker]
        # update current ticker count
        # increment ticker index; if current ticker index exceeds list, then loop back to the first item
        current_ticker = current_ticker + 1
        if current_ticker > (len(selected_ticker) - 1):
            current_ticker = 0

    # Depending on the ticket name length, resize the text
    ticker_short_name = str(yf.Ticker(symbol).info['shortName']).removesuffix(', Inc.').removesuffix('index').\
        removesuffix('average').removesuffix('Inc.').removesuffix('Company').removesuffix('& Co.').removesuffix(', plc.').\
        removesuffix('Corporation').removesuffix('Corp.')
    ticker_name = '{} ({})'.format('Ticker: ', symbol)
    print(ticker_name)
    if len(ticker_name) >= 35:
        # set font size
        ticker_name_font_size = 28
    else:
        # normal font size
        ticker_name_font_size = 32
    ticker_size_style = {'color': 'white',
                         'fontSize': ticker_name_font_size,
                         'margin': 0,
                         'text-align': 'center'}
    # obtain yahoo finance historic data and ticker text name
    price_history = yf.Ticker(symbol).history(
        period='1d',  # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval='1m', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        actions=False)

    # calculating key price and date information
    opening_price = price_history.iloc[0]["Close"]
    closing_price = price_history.iloc[-1]["Close"]
    time_adjustment = price_history.index.tz_convert(pytz.timezone('America/Vancouver'))

    # obtain yesterday's end price
    ytd_price_history = yf.Ticker(symbol).history(period='5d', interval='1d', actions=False)
    ytd_data_range = len(ytd_price_history) - 2
    ytd_closing_price = ytd_price_history.iloc[ytd_data_range]["Close"]

    # determine if line is green or red based on today's gains or losses
    if (closing_price - ytd_closing_price) > 0:
        color_logic = "green"
    else:
        color_logic = "red"

    # calculate day's gains/loss and percentage change
    price_change = closing_price - ytd_closing_price
    percentage_change = (closing_price - ytd_closing_price) / ytd_closing_price * 100

    # update figure information
    fig = go.Figure(go.Scatter(x=time_adjustment,
                               y=price_history["Close"],
                               mode='lines+markers',
                               line=dict(color=color_logic, width=2)))
    fig.update_layout(xaxis_title="Time",
                      yaxis_title="Price ($)",
                      paper_bgcolor='black',
                      plot_bgcolor='black',
                      font_color='white',
                      font_size=20,
                      autosize=True,
                      height=600)

    # datetime object containing current date and time
    now = datetime.now()
    date = now.strftime("%b-%d, %Y")
    time = now.strftime("%I:%M %p")

    # update figure and Text
    ticker_current_price = '${}'.format(round(closing_price, 2))
    ticker_price_change = '${} ({}%)'.format(round(price_change, 2), round(percentage_change, 2))
    ticker_price_change_style = {'color': color_logic,
                                 'fontSize': 35,
                                 'margin': 0,
                                 'text-align': 'center'}
    return fig, date, time, ticker_name, ticker_size_style,\
           ticker_current_price, ticker_price_change, ticker_price_change_style


# main function for the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.server.run(port=8000, host='xxx.xxx.x.xxx')
