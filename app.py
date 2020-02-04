import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas_datareader as pdr
import datetime

import plotly.graph_objects as go

start_date = datetime.datetime(2015,1,1)
end_date = datetime.datetime(2019,6,30)
ticker = 'TSLA'

df = pdr.data.get_data_yahoo(ticker, start = start_date)


df.reset_index(inplace = True)



layout = dict(title = 'Stoch chart', showlegend = False)
fig = go.Figure(go.Scatter(x = list(df['Date']), y = list(df['Close'])), layout)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server



app.layout = html.Div([   
        html.Div(dcc.Input(id = 'Stock-Ticker', placeholder = 'Enter Stock Ticker', type = 'text', value = 'TSLA' ),),
        
        html.Div([
        html.Div(dcc.Graph(id = 'Stock Chart Close', figure = fig), className = 'six columns'),
        html.Div(dcc.Graph(id = 'Stock Chart Returns', figure = fig), className = 'six columns'),
                ], )

        ])


if __name__ == '__main__':
    app.run_server(debug = True)
    
