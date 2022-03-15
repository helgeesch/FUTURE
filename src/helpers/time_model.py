import pandas as pd


def datetime_index_to_hour_of_year(df):
    dff = df.copy()
    ref = pd.Timestamp('2018-01-01 00:00:00')
    dff.loc[:, 'year'] = dff.index.year
    hour_of_year = lambda x: (x.replace(year=2018) - ref).total_seconds() / 3600
    dff.loc[:, 'hour_of_year'] = dff.index.map(hour_of_year).astype(int) + 1
    dff = dff.set_index(['year', 'hour_of_year'])
    return dff
