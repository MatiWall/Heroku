import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class monte_carlo:
    
    
    def __init__(self, df):
        
        self.df = df
        
        
    def GBM(self, simulations = 500, forcast_steps = 50, dt=1):
        ''' 
        GBM: Geometric Brownian Motion.
        '''
        
        last_price = self.df.iloc[-1]
        last_date = self.df.index[-1]
        
        

        returns = self.df.pct_change()
        daily_std = returns.std()
        daily_mean = returns.mean()
        

        df_simulations = pd.DataFrame( index = [ last_date + pd.Timedelta(days=dt*x) for x in range(forcast_steps)])
    
        for x in range(simulations):
        
            price_series = []
            price = last_price * np.exp( (daily_mean-daily_std**2.0/2.0)* dt + daily_std *np.sqrt(dt) *np.random.normal(0, 1))
            price_series.append(price)
        
            for i in range(forcast_steps-1):
            
                price = price_series[i]*np.exp( (daily_mean-daily_std**2.0/2.0)* dt + daily_std *np.sqrt(dt) *np.random.normal(0, 1))
                price_series.append(price)
             
        
            df_simulations[x] = price_series
        
            
        self.df_simulations = df_simulations
        
       
		
    def plot_simulation(self):
      
        fig = make_subplots(rows=1, cols=2, shared_xaxes = False, vertical_spacing=0.03,horizontal_spacing=0.009)
        
        for name, data in self.df_simulations.iteritems():
            fig.add_trace({'x': data.index,'y': data.values,'type':'scatter', 'showlegend' : False},
                         row = 1, col = 1, secondary_y=False)
            if name > 200:
                break
            
            
        df_simulations_end = self.df_simulations.iloc[-1, :]  

        fig.add_trace({'x':  df_simulations_end.values, 'type':'histogram', 'showlegend' : False,  'xbins' : {'size' : 25},  'histnorm' : "probability", },
                         row = 1, col = 2, secondary_y=False)
        
        
        #self.kde()
        
        return fig
    
    
    def kde(self, h = 1, kernel = 'gaussian'):
        
        data = self.df_simulations.iloc[-1,:].to_numpy()
        
        if kernel == 'gaussian':
            K = lambda x : np.sum(np.exp(-(np.subtract(x,data.transpose()))**2/h))
        else:
            print('Choose Kernel')
    
        range_min = data.min()
        range_max = data.max()
        
        range_data = np.linspace(range_min, range_max, 100)
        
        kde_dist = K(range_data)
        
        print(kde_dist)
        return kde_dist

    
    
    
    def return_data(self):
        return self.df_simulations
    
    