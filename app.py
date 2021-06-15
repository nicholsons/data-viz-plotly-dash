import dash
import dash_html_components as html

# Creates the Dash web app
app = dash.Dash(__name__)

# Defines the layout of the page. Uses python methods to generate HTML.
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
])

# Runs the web app. By default you should be able to access it at http://127.0.0.1:8050/ in a web browser
if __name__ == '__main__':
    app.run_server(debug=True)
