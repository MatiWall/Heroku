import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from .plots import timeseries_plot

import pandas_datareader as pdr


nasdaq_tickers = pdr.nasdaq_trader.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)

names = nasdaq_tickers['Security Name']
tickers = nasdaq_tickers['NASDAQ Symbol']
options_ticker = [{'label' : name, 'value' : ticker } for (name, ticker) in zip(names.to_list(), tickers.to_list())]
options_price = [{'label': 'Highest Daily Price', 'value': 'High'}, {'label': 'Lowest Daily Price', 'value': 'Low'}, 
                 {'label': 'Open Price', 'value': 'Open'}, {'label': 'Close Price', 'value': 'Close'}, {'label': 'Adjusted Close Price', 'value': 'Adj Close'}]



layout = html.Div([
    html.H3('Timeseries Analysis of Longterm Stocks'),
    html.Div([
    html.Div([dcc.Dropdown(
            id="input-ticker",
            options = options_ticker,
            placeholder="Select one or more companies",
            multi = True,
            value='TSLA'
        ), 
             dcc.Checklist(
             id='OHLC',
             options=[{'label': i, 'value': i} for i in ['Close', 'Open', 'High', 'Low', 'Adj Close']],
             labelStyle={'display': 'inline-block'},  
             value = ['Close']
             )  


    ], className = 'six columns'), html.Br(), html.Br()
                    ]),
    html.Br(),     
    html.Div(id = 'stock-plot'),
    dcc.Link('Go to App 2', href='/apps/app2')
])


@app.callback(# Callback that loads chosen data
    Output('stock-plot', 'children'),
    [Input('input-ticker', 'value'), Input('OHLC', 'value')])
def display_value(values, OHLC):

    try:
        if isinstance(values, str):
            df = pdr.data.get_data_yahoo(values)
            plot = timeseries_plot( df )
        elif isinstance(values, list):
            data_frames = [pdr.data.get_data_yahoo(value) for value in values]
            plot = timeseries_plot(data_frames[0] )
            
        
        figure = plot.plot()
        
        figure = plot.add_plot(figure, OHLC)
        
        
        
        
        figure = dcc.Graph( figure = figure)
    
    except:
        figure = dcc.Graph()
    
    
    return  figure

