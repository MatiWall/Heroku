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
fig = go.Figure([go.Scatter(x = df['Date'], y = df['Close'])])

layout = dict(title = 'Stoch chart', show_legend = False)



app = dash.Dash()

server = app.server

app.layout = html.Div([
        
        html.H1(children = 'Hello World'),
        html.H1(dcc.Graph(id = 'Stock Chart', figure = fig)),
                ])

if __name__ == '__main__':
    app.run_server(debug = True)
    