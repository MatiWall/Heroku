import plotly.graph_objects as go
import pandas as pd
#import plotly.tools as tls
from plotly.subplots import make_subplots


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
        self.price = price
     
        fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.03,horizontal_spacing=0.009,
                            specs=[[{"secondary_y": False}],
                                   [{"secondary_y": True, "rowspan": 3}],  
                                   [None],
                                   [None],
                                   [{"secondary_y": False}] ],
                                   )
                               
        
        
        fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
        fig['layout']['yaxis2']['showgrid'] = False
        
        
        fig.add_trace({'x':self.df.index,'y':self.df.Volume,'type':'bar','name':'Volume', 'showlegend' : False, 'marker' :{'color' : 'red'}},
                         row = 2, col = 1, secondary_y=False)
        fig.update_yaxes(title_text='Volume', row = 2, col = 1, secondary_y=False)
        fig.update_yaxes(title_text='Price', row = 2, col = 1, secondary_y=True)
      
     
        
        
        rsi = self.rsiFunc()
        fig.add_trace({'x' : rsi.index,'y' : rsi.values, 'type' : 'scatter', 'name':'rsi', 'showlegend' : False, 'marker' :{'color' : 'red'}},
                         row = 1, col = 1)
        
        fig.update_yaxes(title_text="RSI",  range=[0, 120], row = 1, col = 1)
                        
    
        line30 = pd.Series([30, 30], index = [self.df.index[0], self.df.index[-1]])
        line70 = pd.Series([70, 70], index = [self.df.index[0], self.df.index[-1]])
        fig.add_trace({'x' : line30.index,'y' : line30.values , 'type' : 'scatter',  'mode' : 'lines',
                      'showlegend' : False, 'marker' :{'color' : 'black'}}, row = 1, col = 1)
                        
        fig.add_trace({'x' : line70.index,'y' : line70.values , 'type' : 'scatter', 'mode' : 'lines',
                      'showlegend' : False, 'marker' :{'color' : 'black'}}, row = 1, col = 1)
                        
        
                 
                    
        histogram, signalLine, macd = self.computeMACD()
        fig.add_trace({'x' : macd.index,'y' : macd.values, 'type' : 'scatter', 'name':'MACD-line', 'showlegend' : True, 'marker' :{'color' : 'red'}},
                         row = 5, col = 1)
        fig.add_trace({'x' : signalLine.index,'y' : signalLine.values, 'type' : 'scatter', 'name':'signal line', 'showlegend' : True, 'marker' :{'color' : 'green'}},
                         row = 5, col = 1)
        
        fig.add_trace({'x' : histogram.index,'y' : histogram.values,'type' : 'scatter', 'name':'histogram', 'showlegend' : True, 
                       'marker' :{'color' : 'blue'}, 'fill' : 'tozeroy', 'opacity' : 0.1},
                         row = 5, col = 1)
        
    
        
        fig.update_yaxes(title_text="MACD", row = 5, col = 1)
        fig.update_xaxes(title_text="Date", row = 5, col = 1)                
              
        
        return fig
    
    
    
    def add_plot(self, fig, prices):
        
        for price in is_list(prices):
            fig.add_trace({'x':self.df.index,'y':self.df[price],'type':'scatter','name': price}, row = 2, col = 1, secondary_y = True)
        
        return fig
        
    
    
    def bollinger_bands(self, fig, window = 40, no_std = 2, center = False):
        df_rm = self.df.rolling(window, center = center).mean()
        rolling_std = self.df.rolling(window, center = center ).std()
        
        price = self.price
        
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price], 'name' : 'mavg'  }, row = 2,col = 1, secondary_y = True)
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price]+rolling_std[price]*no_std, 'name' : 'Bb Upper'  }, row = 2, col =1, secondary_y = True)
        fig = fig.add_trace({'x' : df_rm.index, 'y' : df_rm[price]-rolling_std[price]*no_std, 'name' : 'Bb Lower'  }, row = 2, col = 1, secondary_y = True)
        
        return fig
        
    
    
    
    def rsiFunc(self, window = 14):
        price = self.price
        
        delta = self.df[price].diff()
        up_days = delta.copy()
        up_days[delta<=0]=0.0
        down_days = abs(delta.copy())
        down_days[delta>0]=0.0
        RS_up = up_days.rolling(window).mean()
        RS_down = down_days.rolling(window).mean()
        rsi = 100-100/(1+RS_up/RS_down)

        return rsi
    	
    	
 
    
    def computeMACD(self, slow=26, fast=12):
        """
        compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """
        emaslow = self.ExpMovingAverage(self.df[self.price], window = slow)
        emafast = self.ExpMovingAverage(self.df[self.price], window = fast)
        
        MACD_Line = emafast - emaslow
        
        signalLine = self.ExpMovingAverage(MACD_Line, window = 9)
        
        histogram = MACD_Line - signalLine
        
        return histogram, signalLine, MACD_Line
    
    

    
    def candlestick(self):
        
        fig = go.Figure(data=[go.Candlestick(x=self.df.index,
                open=self.df['Open'],
                high=self.df['High'],
                low=self.df['Low'],
                close=self.df['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)

        return fig
    
    
    
    
    @staticmethod
    def ExpMovingAverage(df, window = 20):
        return df.ewm(span = window, adjust=False).mean()
    

def is_list( value ):
    if isinstance(value, list):
        pass
    elif isinstance(value, str):
        value = [value]
            
    return value
        
    
    
