import pandas as pd


def aggregate_pecd_zones_by_country(df, method='sum'):
    """ The PECD in it's raw format is split to the PECD zones Aggregates PECD zones by country.
    :param df: pd.DataFrame
    :param method: str ('sum' or 'mean')
    :return: pd.DataFrame
    """
    if 'region' not in df.columns.names:
        print('region not found in column levels')
        return df
    lvl = df.columns.names.index('region')
    if len(df.columns.names) == 1:
        df.columns = [(i,) for i in df.columns.values]
        df.columns.names = ['region']
    cols = [list(tup)+[tup[lvl]] for tup in df.columns.values]
    for i in range(len(cols)):
        cols[i][lvl] = cols[i][lvl][:2]
    df.columns = pd.MultiIndex.from_tuples(cols, names=list(df.columns.names)+['temp'])
    on_levels = list(df.columns.names)
    on_levels.remove('temp')
    if method == 'sum':
        df = df.sum(level=on_levels, axis=1)
    else:  # (method == 'mean')
        df = df.mean(level=on_levels, axis=1)
    return df