import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from apps import app1, app2


header_style = {'text-align': 'center', 'color': 'white' , 'backgroundColor':'dodgerblue', 'fontSize' : 40, 'font-weight': 'bold', 'font-style': 'italic', 'marginBottom': 0, 'marginTop': 0, 'border-radius': 5,}

navigation_buttom_style ={'text-align': 'center', 'color': 'white', 'fontSize' : 25, 'marginBottom': 0, 'marginTop': 0, 'border-radius': 2, 'backgroundColor':'dodgerblue'}
navigation_style = {'backgroundColor':'dodgerblue'}


app.layout = html.Div([
	html.H1('K&M Investments',  style= header_style),
    dcc.Location(id='url', refresh=False),
    html.Div(html.Nav([	html.Div(dcc.Link('Home', href='/', style = navigation_buttom_style), className = 'nav-item nav-link btn'), 
    		  	html.Div( dcc.Link('Stock', href='/apps/app1', style = navigation_buttom_style), className = 'nav-item nav-link btn'), 
    		  	html.Div( dcc.Link('Intraday', href='/apps/app2', style = navigation_buttom_style), className = 'nav-item nav-link btn')], style = navigation_style)),
    		  	
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
