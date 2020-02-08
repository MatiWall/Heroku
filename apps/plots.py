import plotly.graph_objects as go
import pandas as pd
import plotly.tools as tls

import dash_core_components as dcc


class timeseries_plot:
    
    def __init__(self, df,  ticker = 'TSLA', window = 50):
        
        self.df = df
        self.ticker = ticker
            
        self.rolling_mean = True
        self.window = window 
    
        self.start = None
        self.end = None 
    
    def plot(self, price = 'Close', rolling_mean = True, **kwargs):
       
     
        fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.009,horizontal_spacing=0.009)
        fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
 
        fig.append_trace({'x':self.df.index,'y':self.df[price],'type':'scatter','name':price},1,1)
        fig.update_yaxes(title_text = 'Price', row=1, col=1)
        
        
        fig.append_trace({'x':self.df.index,'y':self.df.Volume,'type':'bar','name':'Volume'},2,1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text='Counts', row=2, col=1)
        
        if rolling_mean:
            df_rm = self.df.rolling(self.window, center = True).mean()
            fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price], 'name' : 'mavg'  }, 1,1)
        
        return fig
    
    

