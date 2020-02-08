import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from .plots import timeseries_plot

import pandas_datareader as pdr


nasdaq_tickers = pdr.nasdaq_trader.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)

names = nasdaq_tickers['Security Name']
tickers = nasdaq_tickers['NASDAQ Symbol']
options = [{'label' : name, 'value' : ticker } for (name, ticker) in zip(names.to_list(), tickers.to_list())]




layout = html.Div([
    html.H3('Timeseries Analysis of Longterm Stocks'),
        html.Div(dcc.Dropdown(
            id="input-ticker",
            options = options,
            placeholder="Select one or more companies",
            multi = True,
            value='TSLA'
        )
    )
    ,
    html.Div(id = 'stock-plot'),
    dcc.Link('Go to App 2', href='/apps/app2')
])


@app.callback(# Callback that loads chosen data
    Output('stock-plot', 'children'),
    [Input('input-ticker', 'value')])
def display_value(value):
    try:
        if isinstance(value, str):
            df = pdr.data.get_data_yahoo(value)
            plot = timeseries_plot( df, 'test')
        elif isinstance(value, list):
            data_frames = [pdr.data.get_data_yahoo(val) for val in value]
            plot = timeseries_plot(data_frames[0], 'test')
    except:
        plot = None 
    
    
    print(value)
    return  dcc.Graph( figure = plot.plot())

