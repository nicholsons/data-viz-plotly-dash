import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd


def prepare_data():
    data_raw = pd.read_csv(
        "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_global.csv")
    print(list(data_raw.columns))
    date_start = data_raw[5]
    date_end = pd.colnames(data_raw)[pd.ncol(data_raw)]
    return data_raw


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(children=[
    html.H1("Hello Dash"),
],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
