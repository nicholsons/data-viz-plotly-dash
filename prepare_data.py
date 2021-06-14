import pandas as pd
import plotly.graph_objects as go


def clean_data(data_raw):
    """Return melted dataframe and set index"""
    df = data_raw.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_name='Cases', var_name='Date')
    df = df.set_index(['Country/Region', 'Province/State', 'Date'])
    return df


def consolidate_country_data(data_cleaned):
    """Return country-wide data rather than by region"""
    df = data_cleaned.groupby(['Country/Region', 'Date'])['Cases'].sum().reset_index()
    df = df.set_index(['Country/Region', 'Date'])
    df.index = df.index.set_levels([df.index.levels[0], pd.to_datetime(df.index.levels[1])])
    df = df.sort_values(['Country/Region', 'Date'], ascending=True)
    return df


def get_top_10_country_list(country_data):
    """Returns dataframe for top 10 countries sorted by maximum cases"""
    df = country_data.max(level=0)['Cases'].reset_index().set_index('Country/Region')
    df.sort_values(by='Cases', ascending=False, inplace=True)
    df_top_10 = df.head(10)
    return df_top_10.index.tolist()


def create_chart(country_data, country_list):
    figure = go.Figure()

    for country in country_list:
        country_first_case = country_data.loc[country]['Cases'].reset_index().set_index('Date')
        country_growth = country_first_case[country_first_case.gt(99)].dropna().reset_index()
        figure.add_trace(go.Scatter(x=country_growth.index, y=country_growth['Cases'], mode='lines', name=country))
        length = len(country_growth.index) - 1
        figure.add_annotation(
            x=length,
            y=country_growth.at[length, 'Cases'],
            text=country,
            showarrow=False,
            xshift=15)

    figure.update_layout(
        title="COVID-19 cumulative number of cases",
        xaxis_title="Day after first 100 cases",
        yaxis_title="Number of cases",
        title_font_size=18,
        xaxis=dict(
            showline=False,
            showgrid=True,
            showticklabels=True,
            gridcolor='lightgrey',
            linewidth=2,
            ticks=None,
            tickfont=dict(
                family='Arial',
                size=12,
                color='darkgrey',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
            gridcolor='lightgrey',
            linewidth=2,
            ticks=None,
            tickfont=dict(
                family='Arial',
                size=12,
                color='darkgrey'
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
        plot_bgcolor='#fff1e5'
    )

    return figure


def add_range_slider(figure):
    figure.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
        )
    )
    return figure


if __name__ == '__main__':
    df_raw = pd.read_csv(
        "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_global.csv")
    df_cleaned_data = clean_data(df_raw)
    df_country_data = consolidate_country_data(df_cleaned_data)
    top_10_country_list = get_top_10_country_list(df_country_data)
    fig = create_chart(df_country_data, top_10_country_list)
    fig.show()
