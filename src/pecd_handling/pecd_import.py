import os
import time
import pandas as pd


PECD_TECHS = ['PV', 'Offshore', 'Onshore']  # optionally you could also add 'CSP' here



def read_pecd_xls_file(path):
    """ Reads one xls file in the PECD format and combines all sheets to a dataframe.
    :param path: str (file should be in folder)
    :return: pd.DataFrame
    """
    print("Now opening file:", path)
    csv_filepath = path.replace('.xlsx', '.csv')
    # pickle_filepath = path.replace('.xlsx', '.pkl')
    if os.path.isfile(csv_filepath):
        print("Cached .csv version found, this import will be fast.")
        df = pd.read_csv(csv_filepath, index_col=0, header=[0], parse_dates=True)
        df.columns.name = 'region'
    else:
        print("Seems like you are importing for the first time, this may take up to an hour. "
              "Future imports will be faster as we are storing a .csv version.")
        start_time = time.time()
        xls = pd.read_excel(path, sheet_name=None, skiprows=10)
        print(f"File {path} took {(time.time() - start_time)/60:.1f} minutes to load")
        for sheet in list(xls.keys()):
            # Let's drop sheets that are empty (some PECD zones are empty in the DB)
            if xls[sheet].dropna().empty or sheet in []:  # list of sheetnames that do not contain PECD timeseries.
                del xls[sheet]
        regions = xls.keys()
        df = pd.concat([sheet_to_series(xls[r]) for r in regions], keys=[r for r in regions], names=['region'], axis=1)
        df.to_csv(csv_filepath)
    return df


def sheet_to_series(sheet):
    """ Turns one sheet of a PECD excel file into a pandas Series with datetime index.
    :param sheet: pd.DataFrame
    :return: pd.Series
    """
    sheet[['day', 'month']] = sheet.Date.str.split(".", n=1, expand=True)
    sheet.month = sheet.month.str.split('.').str[0]#.strip('.')
    sheet.dropna(inplace=True)
    sheet.drop(labels=['Date'], axis=1, inplace=True)
    sheet.rename(columns={'Hour': 'hour'}, inplace=True)
    sheet['hour'] = sheet['hour'].astype(int) - 1
    sheet = sheet.set_index(['month', 'day', 'hour'])
    sheet.columns.name = 'year'
    sheet = sheet.stack('year')
    sheet = sheet.reorder_levels(['year', 'month', 'day', 'hour'])
    sheet.index = pd.to_datetime(pd.DataFrame(sheet.index.to_list(), columns=sheet.index.names)).values
    sheet = sheet.sort_index()
    return sheet
