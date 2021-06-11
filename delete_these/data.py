import pandas as pd
import plotly.graph_objects as go


def clean_data(df_raw):
    """Return melted dateframe and set index"""
    df = df_raw.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_name='Cases', var_name='Date')
    df = df.set_index(['Country/Region', 'Province/State', 'Date'])
    return df


def consolidate_country_data(df_cleaned):
    """Return country-wide data rather than by region"""
    df = df_cleaned.groupby(['Country/Region', 'Date'])['Cases'].sum().reset_index()
    df = df.set_index(['Country/Region', 'Date'])
    df.index = df.index.set_levels([df.index.levels[0], pd.to_datetime(df.index.levels[1])])
    df = df.sort_values(['Country/Region', 'Date'], ascending=True)
    return df


def get_top_10_country_list(df_country_data):
    """Returns dataframe for top 10 countries sorted by maximum cases"""
    df = df_country_data.max(level=0)['Cases'].reset_index().set_index('Country/Region')
    df.sort_values(by='Cases', ascending=False, inplace=True)
    df_top_10 = df.head(10)
    return df_top_10.index.tolist()


# TODO: Use df rather than dict
def order_by_day_from_num_cases(top_10_country_list, df_country, num_cases):
    """Returns dict with country names and the data.
    Start defined as the first day more than num_cases were reported"""

    top_10_growth = {}

    for country in top_10_country_list:
        country_first_case = df_country.loc[country]['Cases'].reset_index().set_index('Date')
        country_growth = country_first_case[country_first_case.gt(num_cases)].dropna().reset_index()
        top_10_growth[country] = country_growth

    return top_10_growth


def create_chart(country_growth, country_list):
    fig = go.Figure()

    for country in country_list:
        country_first_case = country_growth.loc[country]['Cases'].reset_index().set_index('Date')
        country_growth = country_first_case[country_first_case.gt(99)].dropna().reset_index()
        fig.add_trace(go.Scatter(x=country_growth.index, y=country_growth['Cases'], mode='lines', name=country))
        length = len(country_growth.index) - 1
        fig.add_annotation(
            x=length,
            y=country_growth.at[(length), 'Cases'],
            text=country,
            showarrow=False,
            xshift=10)

    fig.show()

    fig.update_layout(
        title="COVID-19 cumulative number of cases",
        xaxis_title="Day after first 100 cases",
        yaxis_title="Number of cases",
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=100,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )


if __name__ == '__main__':
    df_raw = pd.read_csv(
        "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_global.csv")
    df_cleaned = clean_data(df_raw)
    df_country = consolidate_country_data(df_cleaned)
    top_10_country_list = get_top_10_country_list(df_country)
    top_10_growth = order_by_day_from_num_cases(top_10_country_list, df_country, 99)
    create_chart(top_10_growth, top_10_country_list)