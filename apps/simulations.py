import pandas as pd

import plotly.figure_factory as ff
from datetime import datetime, timedelta 

class monte_carlo:
    
    
    def __init__(self, df, start, end):
        
        self.df = df
        self.start = start
        self.end = end
        
        
    def GBM(self, simulations = 100, forcast_steps = 50, dt=1):
        ''' 
        GBM: Geometric Brownian Motion.
        '''
        
        last_price = self.df.iloc[-1]
        last_date = self.df.index[-1]
        
        

        returns = self.df.pct_change()
        daily_std = returns.std()
        daily_mean = returns.mean()
        
        forcast_steps = int(np.ceil(self.forecast_days/dt))

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
        
       
       
	def plot(self):
	
		fig = ff.create_distplot(self.df_simulations)
		
		
		return fig
		
	
