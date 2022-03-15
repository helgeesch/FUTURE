import pandas as pd


def add_custom_variable(df, variable_name, sum_of):
    """ Add a custom variable to the dataframe built by a defined sum of existing variables.
    :param df: pd.DataFrame (df with all data)
    :param variable_name: str (name of new variable (e.g. netload))
    :param sum_of: dict (multipliers for the existing variables to sum together for new variable (e.g. {'load': 1, 'pv':-1, ...}))
    :return: pd.DataFrame
    """
    multiplier = pd.Series(sum_of, name='variable')
    on_levels = list(df.columns.names)
    on_levels.remove('variable')
    dff = df.multiply(multiplier, axis=1, level='variable').dropna(axis=1).sum(axis=1, level=on_levels)
    dff = pd.concat([dff], keys=[variable_name], names=['variable'], axis=1)
    dff = dff.reorder_levels(df.columns.names, axis=1)
    df = pd.concat([df, dff], axis=1)
    df = df.sort_index(axis=1)
    return df
