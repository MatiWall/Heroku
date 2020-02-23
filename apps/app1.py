import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from .plots import timeseries_plot, is_list
from .simulations import monte_carlo

import pandas_datareader as pdr
import pandas as pd


nasdaq_tickers = pdr.nasdaq_trader.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)

names = nasdaq_tickers['Security Name']
tickers = nasdaq_tickers['NASDAQ Symbol']
options_ticker = [{'label' : name, 'value' : ticker } for (name, ticker) in zip(names.to_list(), tickers.to_list())]
options_price = [{'label': 'Highest Daily Price', 'value': 'High'}, {'label': 'Lowest Daily Price', 'value': 'Low'}, 
                 {'label': 'Open Price', 'value': 'Open'}, {'label': 'Close Price', 'value': 'Close'}, {'label': 'Adjusted Close Price', 'value': 'Adj Close'}]



layout = html.Div([
    html.H3('Investments'),
    html.Div([
            html.Div(id = 'content', children = 
                     [dcc.Dropdown( id="inputCompanyName",
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
                     , 
             dcc.Input(
            id ='inputCompanyTicker',
            type = 'text',
            debounce = True, 
            multiple = True,
            placeholder = 'Input Ticker',
        )   ], className = 'six columns'), html.Br(), html.Br()
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
    
    ])
    , html.Br(),
    html.Div([
            dcc.Checklist( id='montecarlo',
                                   options=[{'label': 1, 'value': 0}],
                                   labelStyle={'display': 'inline-block'},  
                                   )  ,
            
            html.Div(id = 'montecarloPlot', className = 'ten columns'),]),
    dcc.Link('Go to App 2', href='/apps/app2')
    
    
])


@app.callback(# Callback that loads chosen data
    Output('intermediate-data-value', 'children'),
    [Input('inputCompanyName', 'value'), Input('inputCompanyTicker', 'value')])
def display_value(dropDownTickers, inputTickers ):
    
    
    if dropDownTickers is None and inputTickers is None:
    
        return None
    elif dropDownTickers is None:
        tickers = is_list(inputTickers)
    elif inputTickers is None:
        tickers = is_list(dropDownTickers)
    else:
        tickers = is_list(inputTickers) + is_list(dropDownTickers)
    
  
        

    df_data = pd.DataFrame()
    for value in tickers:
        try:
            df = pdr.data.get_data_yahoo(value)
            df['Ticker'] = value
            df_data = df_data.append(df)
        except:
            print('Invalid ticker {}'.format(value))
        
    return  df_data.to_json(date_format='iso', orient='split')


@app.callback(
        Output('stock-plot', 'children'),
        [Input('OCLH', 'value'), Input('intermediate-data-value', 'children'), Input('technical-indicators', 'value')]
        )
def plot_data(OCLH, jsonified_data, technical_indicators):
    
    
     
    df = pd.read_json(jsonified_data, orient='split')
    
    try:
        gb = df.groupby(['Ticker'])
    
        plots = []
        for name, group in gb:
            
            plotly_graph = timeseries_plot(group) 
            figure = plotly_graph.plot() 
            figure = plotly_graph.add_plot(figure, OCLH)  
     
            if technical_indicators:
                figure = plotly_graph.bollinger_bands(figure)
        
            graph = dcc.Graph( figure = figure)
        
            plots.append(html.Div(graph))
    except:
        plots =html.H1('No Stock Selected!')
   
    
   

    return plots



@app.callback(
        Output('montecarloPlot', 'children'),
        [Input('montecarlo', 'value'), Input('intermediate-data-value', 'children')]
        )
def plot_montecarlo(value, jsonified_data):
     
    df = pd.read_json(jsonified_data, orient='split')

    mtSim = monte_carlo(df['Close'])
    mtSim.GBM()
    fig = mtSim.plot_simulation()
    print(type(fig))
    return fig

