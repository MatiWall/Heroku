import dash
import dash_html_components as html
import dash_core_components as dcc







import sys # Adding path of custum module
sys.path.append('/home/matias/Documents/Stock_Trading/Heroku/stock_plots/')
import plots




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server



app.layout = html.Div([   
        html.Div(dcc.Input(id = 'Stock-Ticker', placeholder = 'Enter Stock Ticker', type = 'text', value = 'TSLA' ),),
        
        html.Div([
        html.Div(dcc.Graph(id = 'Stock Chart Close', figure = plots.plot_timeseries()), className = 'six columns'),
        html.Div(dcc.Graph(id = 'Stock Chart Returns', figure = plots.plot_timeseries()), className = 'six columns'),
                ], )

        ])


if __name__ == '__main__':
    app.run_server(debug = True)
    

    