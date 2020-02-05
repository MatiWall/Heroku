import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc




import sys # Adding path of custum module
sys.path.append('/home/matias/Documents/Stock_Trading/Heroku/stock_plots/')
import plots



layout = html.Div([
	
		#html.H1('K&M Investments',  style={'text-align': 'center', 'color': 'white' , 'backgroundColor':'dodgerblue', 'fontSize' : 40, 'font-weight': 'bold', 'font-style': 'italic', 'marginBottom': 0, 'marginTop': 0, 'border-radius': 5,}) ,  

        html.Div(dcc.Input(id = 'Stock-Ticker', placeholder = 'Enter Stock Ticker', type = 'text', value = 'TSLA' ),),
        
        html.Div([
        html.Div(dcc.Graph(id = 'Stock Chart Close', figure = plots.plot_timeseries()), className = 'six columns'),
        html.Div(dcc.Graph(id = 'Stock Chart Returns', figure = plots.plot_timeseries()), className = 'six columns'),
                ], )
        ], id = 'home_page')



@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
