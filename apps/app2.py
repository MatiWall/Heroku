import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .plots import timeseries_plot 

from alpha_vantage.timeseries import TimeSeries


from app import app

api_key = 'HU4DVL38WYJOGV06'
ts = TimeSeries(key = api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='TSLA',interval='1min', outputsize='compact')

data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

plot = timeseries_plot(data)

figure = plot.candlestick()



layout = html.Div([
    html.H3('App 2'),
    dcc.Graph(figure = figure),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
