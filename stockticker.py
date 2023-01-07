import dash
import pandas
import pytz
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timezone

# obtain ticker from csv file
ticker_csv_file_name = 'ticker.csv'
df_ticker = pandas.read_csv(filepath_or_buffer=ticker_csv_file_name)
tickers = df_ticker['tickers'].dropna().tolist()
crypto = df_ticker['crypto'].dropna().tolist()
selected_ticker = tickers + crypto
current_ticker = 0

fig = go.Figure()

# set css file
external_stylesheets = ['/assets/page_format.css']

# set dash plotly figures
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H1(id='current_time',
                style={'color': 'white',
                       'fontSize': 80,
                       'text-align': 'center',
                       'padding': 0,
                       'margin': 0}),
        html.Span(id='ticker_text',
                  style={'color': 'white',
                         'fontSize': 40,
                         'text-align': 'left',
                         'padding': 0}),
        html.Span(id='ticker_price',
                  style={'color': 'white',
                         'fontSize': 40,
                         'text-align': 'left',
                         'padding': 50,
                         'margin': 50}),
        html.Span(id='ticker_price_change'),
        dbc.Button('Next', id='btn-next', n_clicks=0),
        dcc.Graph(figure=fig,
                  id='graph'),
        dbc.Row(
            [
                daq.BooleanSwitch(on=True,
                                  label='Play',
                                  id='btn-play',
                                  labelPosition="top",
                                  style={'color': 'white',
                                         'fontSize': 12,
                                         'text-align': 'left',
                                         'padding': 0,
                                         'margin': 0}
                                  ),
                daq.BooleanSwitch(on=False,
                                  label='Crypto Only',
                                  id='btn-crypto',
                                  labelPosition="top",
                                  style={'color': 'white',
                                         'fontSize': 12,
                                         'text-align': 'left',
                                         'padding': 0,
                                         'margin': 0}
                                  ),
                html.Span('test', id='testing')
            ]
        ),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ]),
    style={'backgroundColor': 'black'}
)


# Disable or enable the interval to pause or play the auto refresh
@app.callback([Output('interval-component', 'disabled')],
              [Input('btn-play', 'on')])
def update_global_var(on):
    if on is True:
        print('interval - disable set to False')
        return [False]
    else:
        print('interval - disable set to True')
        return [True]


# update selected ticker list to be crypto or all tickers
@app.callback([Output('testing', 'children')],
              [Input('btn-crypto', 'on')])
def update_global_var(btncrypto):
    global selected_ticker
    global current_ticker
    global tickers
    global crypto

    # if the crypto is selected, update selected ticker list to be crypto only and reset current ticker count
    if btncrypto is True:
        print('ticker - only crypto')
        current_ticker = 0
        selected_ticker = crypto
        return ['crypto']
    # if the crypto is not selected, update selected ticker list to stocks and crypto and reset current ticker count
    else:
        print('ticker - all tickers')
        current_ticker = 0
        selected_ticker = tickers + crypto
        return ['all ticker']


# Multiple components can update everytime interval gets fired.
@app.callback([Output('graph', 'figure'),
               Output('current_time', 'children'),
               Output('ticker_text', 'children'),
               Output('ticker_price', 'children'),
               Output('ticker_price_change', 'children'),
               Output('ticker_price_change', 'style')],
              [Input('interval-component', 'n_intervals'),
               Input('btn-next', 'n_clicks')])
def update_graph(n, btnnext):
    # obtain current loop and tickers
    global current_ticker
    global selected_ticker
    global crypto

    symbol = selected_ticker[current_ticker]

    # obtain yahoo finance historic data
    price_history = yf.Ticker(symbol).history(period='1d',  # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
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
    percentage_change = (closing_price - ytd_closing_price)/ytd_closing_price*100

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

    # update current ticker count
    # increment ticker index; if current ticker index exceeds list, then loop back to the first item
    current_ticker = current_ticker + 1
    if current_ticker > (len(selected_ticker) - 1):
        current_ticker = 0

    # datetime object containing current date and time
    now = datetime.now()
    date = now.strftime("%b-%d, %Y")
    time = now.strftime("%I:%M %p")
    date_time_text = '{} {} {}'.format(date, '--', time)

    # update figure and Text
    symbol_text = 'Ticker: {}'.format(symbol)
    ticker_current_price = '${}'.format(round(closing_price, 2))
    ticker_price_change = '${} ({}%)'.format(round(price_change, 2), round(percentage_change, 2))
    ticker_price_change_style = {'color': color_logic,
                                 'fontSize': 40,
                                 'margin': 20}
    return fig, date_time_text, symbol_text, ticker_current_price, ticker_price_change, ticker_price_change_style


# main function for the dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
