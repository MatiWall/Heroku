import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2

from app import server # Necessary for heroku deployment


logo_style = {'text-align': 'center', 'color': 'white' , 'backgroundColor':'dodgerblue', 'fontSize' : 40, 'font-weight': 'bold', 'font-style': 'italic', 'marginLeft': 20,}

navigation_buttom_style ={'text-align': 'center', 'color': 'white', 'fontSize' : 20, 'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5, 'marginRight': 5}
navigation_style = {'backgroundColor':'dodgerblue', 'border-radius': 5 , 'marginLeft': 0,}




app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(html.Nav([	html.A('K&M Investments',  style = logo_style), html.A(dcc.Link('Home', href='/', style = navigation_buttom_style), className = 'button', style = {'marginLeft': 30,}), 
    		  	html.A( dcc.Link('Stock', href='/apps/app1', style = navigation_buttom_style), className = 'button'), 
    		  	html.A( dcc.Link('Intraday', href='/apps/app2', style = navigation_buttom_style), className = 'button')], style = navigation_style)),
    		  	
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/':
    	pass
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
