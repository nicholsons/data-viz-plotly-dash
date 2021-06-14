from urllib import error

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import prepare_data

# Global variables for the two charts
msg_no_data = 'No chart to display'
fig_static = go.Figure(data=[go.Table(header=dict(values=[msg_no_data]))])
fig_select = go.Figure(data=[go.Table(header=dict(values=[msg_no_data]))])
df_country_data = pd.DataFrame()
top_10_country_list = []

# Read the John Hopkins dataset, prepare the data and create the chart using functions in prepare_data.py
csv_file = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series" \
           "/time_series_covid19_confirmed_global.csv"

try:
    df_raw = pd.read_csv(csv_file)
    df_cleaned_data = prepare_data.clean_data(df_raw)
    df_country_data = prepare_data.consolidate_country_data(df_cleaned_data)
    top_10_country_list = prepare_data.get_top_10_country_list(df_country_data)
    fig_static = prepare_data.create_chart(df_country_data, top_10_country_list)
except (FileNotFoundError, error.HTTPError) as e:
    print("Could not find file:", csv_file, e)

# Create the Dash app instance and use the Bootstrap stylesheet theme
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the webpage, describe each of the HTML elements and charts
app.layout = dbc.Container(children=[
    html.H1("COVID-19 Dashboard"),
    html.H2("Example of a static chart"),
    dcc.Graph(figure=fig_static),
    html.H2("Example of an interactive chart (using Dash callbacks"),
    dbc.FormGroup([
        html.H4("Select countries"),
        # Dropdown that allows multiple selections
        dcc.Dropdown(id="dd_countries",
                     options=[{"label": x, "value": x} for x in top_10_country_list],
                     value=[],
                     multi=True)
    ]),
    # `id` is used to allow the element to be selected for the callback
    dcc.Graph(id='fig_selected_countries',
              figure=fig_select),
],
    fluid=True,
)


@app.callback(Output('fig_selected_countries', 'figure'), [Input('dd_countries', 'value')])
def plot_selected_countries(selected_countries):
    fig_select_updated = prepare_data.create_chart(df_country_data, selected_countries)
    prepare_data.add_range_slider(fig_select)
    return fig_select_updated


if __name__ == '__main__':
    app.run_server(debug=True)