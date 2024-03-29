
from app import app, dcc, html, Input, Output
from pages import surveillance


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return surveillance.layout
    elif pathname == '/surveillance':
        return surveillance.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
