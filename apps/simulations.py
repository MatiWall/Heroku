import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import cufflinks as cf

class monte_carlo:
    
    
    def __init__(self, df):
        
        self.df = df
        
        
    def GBM(self, simulations = 100, forcast_steps = 50, dt=1):
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
      
        #fig = make_subplots(rows=2, cols=2, shared_xaxes = False, vertical_spacing=0.03,horizontal_spacing=0.009)
        
        plot = self.df_simulations.iplot(kind='scatter')
        print(type(plot))
        
        pass
    
    def return_data(self):
        return self.df_simulations
    
    