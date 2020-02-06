import plotly.graph_objects as go
import pandas_datareader as pdr
import pandas as pd

import time
import dash_core_components as dcc


class timeseries_plot:
    
    def __init__(self, ticker = 'TSLA', window = 50):
        
        self.df = pdr.data.get_data_yahoo(ticker)
        self.ticker = ticker
            
        self.rolling_mean = True
        self.window = window 
    
        self.start = None
        self.end = None 
    
    def plot(self, price = 'Close', rolling_mean = True, **kwargs):
        layout =  go.Layout( margin={'t': 30, 'b' : 5, 'r' : 5, 'l' : 5}, xaxis_title = 'Date', yaxis_title = price, title = self.ticker)
    		
        fig = go.Figure(go.Scatter(x = list(self.df.index), y = list(self.df[price])), {})
        fig.layout = layout
        
        if rolling_mean:
            df_rm = self.df.rolling(self.window, center = True).mean()
            fig.add_trace(go.Scatter(x = df_rm.index, y = df_rm[price] ))
        
        return fig

    def Date_range_slider(self):
        
        date_range = self.df.index
        nth = 100
        
        unixTimeMillis = lambda x : int(time.mktime(x.timetuple()))
        unixToDatetime = lambda x : int(pd.to_datetime(x,unit='D'))
        getmarks = {i : date for i, date in enumerate(date_range) if i%nth == 1}
        
        slider = dcc.RangeSlider(
                id='year_slider',
                min = int(unixTimeMillis(date_range.min())),
                max = int(unixTimeMillis(date_range.max())),
                value = [unixTimeMillis( date_range.min()) , unixTimeMillis( date_range.min() )],
                marks=getmarks
            )
        print(time.localtime( unixToDatetime(slider.min)))
        return slider

