import pandas as pd


def prepare_data():
    data_raw = pd.read_csv(
        "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_global.csv")
    date_start = data_raw.columns[5]
    date_end = data_raw.columns[1]
    # Rename column names
    data = data_raw.rename(columns={"Country / Region": "country", "Province / State": "area"})
    # aggregate data per country
    data = data.group_by('country').sum()
    print(data)
    # TBC: work out what this is doing! summarise_at(vars(!!date_start:!!date_end), sum)

    # Pick countries to highlight
    # arrange country by total number of cases in the last day
    data.sort_values(by=['date_end'], inplace=True, ascending=False)

    # Find top 10 countries with most cases
    top_countries = data.loc[1:10, ['country']]

    # Subset data to include only selected countries
    data_top_countries = data['country'].isin(top_countries)

    # Transpose the data
    data_long = data_top_countries['date_start'].transpose()

    # Change the date format to mdy

# Count day after first N case
min_N <- 100

data_plot <- data_long %>%
  filter(N >= min_N) %>%
  # group by country
  group_by(country) %>%
  mutate(day = seq_along(date))

    return data_raw


def create_plot(data_plot):
    ggplot(
        data=data_plot,
        mapping=aes(
            x=day,
            y=N,
            color=country,
            label=country,
            group=country)
    ) +
    # create line chart
    geom_line() +
    # create scatter plot
    geom_point() +
    # add country label
    geom_text(data=. % > % group_by(country) % > % filter(day == max(day))) +
    # tranform y-axis to log scale
    scale_y_continuous(trans="log2")


if __name__ == '__main__':
    prepare_data()
