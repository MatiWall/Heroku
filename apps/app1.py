import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from .plots import timeseries_plot, is_list

import pandas_datareader as pdr
import pandas as pd


nasdaq_tickers = pdr.nasdaq_trader.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)

names = nasdaq_tickers['Security Name']
tickers = nasdaq_tickers['NASDAQ Symbol']
options_ticker = [{'label' : name, 'value' : ticker } for (name, ticker) in zip(names.to_list(), tickers.to_list())]
options_price = [{'label': 'Highest Daily Price', 'value': 'High'}, {'label': 'Lowest Daily Price', 'value': 'Low'}, 
                 {'label': 'Open Price', 'value': 'Open'}, {'label': 'Close Price', 'value': 'Close'}, {'label': 'Adjusted Close Price', 'value': 'Adj Close'}]



layout = html.Div([
    html.H3('Long Term Stock Trading'),
    html.Div([
            html.Div(id = 'content', children = 
                     [dcc.Dropdown( id="input-ticker",
                                   options = options_ticker,
                                   placeholder="Select one or more companies",
                                   multi = True,
                                   value='TSLA'
                                   ), 
                     dcc.Checklist( id='OCLH',
                                   options=[{'label': i, 'value': i} for i in ['Close', 'Open', 'High', 'Low', 'Adj Close']],
                                   labelStyle={'display': 'inline-block'},  
                                   value = ['Close']
                                   )  
                     ], className = 'six columns'), html.Br(), html.Br()
            ]),
             html.Div(id='intermediate-data-value', style={'display': 'none'}),
             
    html.Br(), html.Div([ 
    html.Div(id = 'stock-plot', className = 'ten columns'),
    html.Div([  html.H5('Technical Indicators'),
    dcc.Checklist(
             id='technical-indicators',
             options=[{'label': i, 'value': i} for i in ['Bollinger Bands']]
             
             ),
            ])
    
    ])  ,
    dcc.Link('Go to App 2', href='/apps/app2')
])


@app.callback(# Callback that loads chosen data
    Output('intermediate-data-value', 'children'),
    [Input('input-ticker', 'value')])
def display_value(values):
    df_data = pd.DataFrame()
    for value in is_list(values):
        df = pdr.data.get_data_yahoo(value)
        df['Ticker'] = value
        df_data = df_data.append(df)
    
    return  df_data.to_json(date_format='iso', orient='split')

@app.callback(
        Output('stock-plot', 'children'),
        [Input('OCLH', 'value'), Input('intermediate-data-value', 'children'), Input('technical-indicators', 'value')]
        )
def plot_data(OCLH, jsonified_data, technical_indicators):
    
     
    df = pd.read_json(jsonified_data, orient='split')
    
    gb = df.groupby(['Ticker'])
    
    
    plots = []
    for name, group in gb:
        
        graph = timeseries_plot(group)
    
        figure = graph.plot()
        
        figure = graph.add_plot(figure, OCLH)  
        
        graph = dcc.Graph( figure = figure)
        plots.append(html.Div(graph))
        
   
    
    if technical_indicators:
        figure = graph.bollinger_bands(figure)

    return plots

