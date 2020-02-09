import plotly.graph_objects as go
import pandas as pd
import plotly.tools as tls

import dash_core_components as dcc


class timeseries_plot:
    '''
    docstring
    
    '''
    
    
    
    def __init__(self, df,  ticker = 'TSLA'):
        
        self.df = df
        self.ticker = ticker
            
        self.rolling_mean = True
    
        self.start = None
        self.end = None 
    
    def plot(self, price = 'Close'):
       
     
        fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.009,horizontal_spacing=0.009)
        
        fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
        fig.update_yaxes(title_text = 'Price', row=1, col=1)
        
        
        fig.append_trace({'x':self.df.index,'y':self.df.Volume,'type':'bar','name':'Volume', 'showlegend' : False, 'marker' :{'color' : 'red'}},2,1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text='Counts', row=2, col=1)
        
        return fig
    
    
    
    def add_plot(self, fig, prices):
        
        for price in is_list(prices):
            fig.append_trace({'x':self.df.index,'y':self.df[price],'type':'scatter','name': price},1,1)
        
        return fig
        
    
    
    def bollinger_bands(self, fig, price = 'Close', window = 40, no_std = 2, center = False):
        df_rm = self.df.rolling(window, center = center).mean()
        rolling_std = self.df.rolling(window, center = center ).std()
        
        
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price], 'name' : 'mavg'  }, 1,1)
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price]+rolling_std[price]*no_std, 'name' : 'Bb Upper'  }, 1,1)
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price]-rolling_std[price]*no_std, 'name' : 'Bb Lower'  }, 1,1)
        
        return fig
        
    
    
    
    
    def candlestick(self):
        
        fig = go.Figure(data=[go.Candlestick(x=self.df.index,
                open=self.df['Open'],
                high=self.df['High'],
                low=self.df['Low'],
                close=self.df['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig
    
    
    
    
    
    

def is_list( value ):
    if isinstance(value, list):
        pass
    elif isinstance(value, str):
        value = [value]
            
    return value
        
    
    