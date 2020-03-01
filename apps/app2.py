import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from .plots import timeseries_plot 

from alpha_vantage.timeseries import TimeSeries


from app import app

api_key = 'HU4DVL38WYJOGV06'
ts = TimeSeries(key = api_key, output_format='pandas')



layout = html.Div([
    html.H3('Intraday Trading'),
      dcc.Input(
            id ='inputCompanyTicker',
            type = 'text',
            debounce = True, 
            multiple = True,
            placeholder = 'Input Ticker',
            value = 'TSLA'
        ),
    html.Div(id = 'intradayPlot'),
    html.Div(id='intermediate-data-intraday', style={'display': 'none'}),
    dcc.Link('Go to App 1', href='/apps/app1')
])


@app.callback(# Callback that loads chosen data
    Output('intermediate-data-intraday', 'children'),
    [Input('inputCompanyTicker', 'value')])
def saveDataLocally(value):

    data, meta_data = ts.get_intraday(symbol = value, interval='1min', outputsize='compact')
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

   
    return  data.to_json(date_format='iso', orient='split')



@app.callback(
    Output('intradayPlot', 'children'),
    [Input('intermediate-data-intraday', 'children')])
def plotData(jsonified_data):
    
    data = pd.read_json(jsonified_data, orient='split')
   
    plot = timeseries_plot(data)
    figure = plot.candlestick()
    plot = dcc.Graph(figure = figure)
    
    return plot
