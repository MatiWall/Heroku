#import pandas as pd
import pandas_datareader as pdr
import datetime

import plotly.graph_objects as go





def plot_timeseries():
    
    start_date = datetime.datetime(2015,1,1)
    end_date = datetime.datetime(2019,6,30)
    ticker = 'TSLA'

    df = pdr.data.get_data_yahoo(ticker, start = start_date)

    
    df.reset_index(inplace = True)
    fig = go.Figure([go.Scatter(x = df['Date'], y = df['Close'])])
    return fig

