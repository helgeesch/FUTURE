import pandas as pd


def add_custom_region(df, name, group, method='sum'):
    """ Add custom regions to the data frame.
    :param df: pd.DataFrame
    :param name: str (name of new region)
    :param group: list (e.g. ['DE', 'AT', 'IT'])
    :param method: str ('mean' or 'sum')
    :return: pd.DataFrame
    """
    on_levels = list(df.columns.names)
    on_levels.remove('region')  # This enables us to have a list with the levels we want to keep separated
    if method == 'mean':
        c = df.loc[:, group].mean(level=on_levels, axis=1)
    elif method == 'sum':
        c = df.loc[:, group].sum(level=on_levels, axis=1)
    c = pd.concat([c], keys=[name], names=['region'], axis=1)
    if len(c.columns.names) > 1:
        c = c.reorder_levels(df.columns.names, axis=1)
    # df = pd.concat([df, c], levels=['region'], axis=1)
    return df.join(c).sort_index(axis=1)