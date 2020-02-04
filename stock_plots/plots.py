import plotly.graph_objects as go
import pandas_datareader as pdr
import datetime



def plot_timeseries(ticker = 'TSLA', roling_mean = True, window = 50, price = 'Close', start_date = None, end_date = None):
    layout = dict(title = 'Stoch chart', showlegend = False)
        
    

    df = pdr.data.get_data_yahoo(ticker, start = start_date, end = end_date)
    
    fig = go.Figure(go.Scatter(x = list(df.index), y = list(df[price])), layout)

    if roling_mean:
        df_rm = df.rolling(window, center = True).mean()
        fig.add_trace(go.Scatter(x = df_rm.index, y = df_rm[price] ))
        
    return fig
