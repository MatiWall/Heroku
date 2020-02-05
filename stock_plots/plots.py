import plotly.graph_objects as go
import pandas_datareader as pdr
import datetime



class timeseries_data:

	def __init__(self, ticker = 'TSLA', rolling_mean = True, window = 50, price = 'Close'):
    
        
    self.df = pdr.data.get_data_yahoo(ticker, start = start_date, end = end_date)
    self.ticker = ticker
    
    self.rolling_mean = True
    self.window = window 
    self.price = price
    
    
    
    def plot(start_date = None, end_date = None):
    
    	fig = go.Figure(go.Scatter(x = list(df.index), y = list(df[price])), layout)

    	if roling_mean:
        	df_rm = df.rolling(window, center = True).mean()
        	fig.add_trace(go.Scatter(x = df_rm.index, y = df_rm[price] ))
        
    return fig
