import numpy as np
import pandas as pd
from scipy.fftpack import rfft, irfft, rfftfreq


# Add default frequency cuts in unit hours, define labels along with it
# two-element list of hourly cuts (e.g. 5-24 hrs)
DURATION_CUTS = {
    'seasonally':   (1*30*24,   1e6),
    'monthly':      (7*24,      1*30*24),
    'weekly':       (24,        7*24),
    'daily':        (4,         24),
    'hourly':       (0.25,      4),
}


def add_decomposed_ts(df, duration_cuts=DURATION_CUTS, remove_dc=True, accumulate_spectra=True):
    """
    Applies Fourier and appends a level to the dataframe with the decomposed time-series in the defined duration cuts.
    Removes the DC component (mean) before applying Fourier.
    :param df: pd.DataFrame (time-series dataframe)
    :param duration_cuts: dict
    :param remove_dc: bool
    :return: pd.DataFrame
    """
    if accumulate_spectra:
        _max = max(i[1] for i in DURATION_CUTS.values())
        duration_cut_values = [(i[0], _max) for i in DURATION_CUTS.values()]
    else:
        duration_cut_values = list(duration_cuts.values())
    freq_cuts = set_frequency_spectrum(duration_cut_values)
    temp = df.copy()
    temp.values[:, :] = rfft(df.subtract(df.mean()).values, axis=0)

    dc_component = 0 if remove_dc else df.mean()
    d = {
        k: process_freq_cut(temp, freq_cuts[i]) + dc_component
        for i, k in enumerate(duration_cuts.keys())
    }
    d.update({f'raw_data': df})
    dff = pd.concat(d, names=['spectrum'], axis=1)
    lvl_order = list(dff.columns.names)
    lvl_order.remove('spectrum')
    lvl_order.append('spectrum')  # So that spectrum is the last level in the dataframe
    dff = dff.reorder_levels(lvl_order, axis=1).sort_index(axis=1)
    return dff


def process_freq_cut(df, freq_cut):
    """
    Cut a time series dataframe into the freq_cut.
    :param df: pd.DataFrame
    :param freq_cut: np.ndarray (shape (2, )) lower and upper cut
    :return: pd.DataFrame
    """
    dT = 3600  # seconds of one time step
    n = len(df)  # window size
    freq = rfftfreq(n, dT)  # frequency vector for fft
    
    temp = df.copy()
    temp[abs(freq) < freq_cut[0]] = 0
    temp[abs(freq) > freq_cut[1]] = 0
    temp.values[:, :] = irfft(temp.values, axis=0)
    return temp


def set_frequency_spectrum(duration_cuts, verbose=True):
    """
    Translates duration cuts into frequency cuts
    :param duration_cuts: list of 2-elements tuples
    :return:
    """
    """ 

    Parameters
    ----------
    duration_cuts : list/bool
        list of duration cuts (each a 2-element list) in hours
    """
    dT = 3600  # seconds of one time step
    freq_cuts = np.sort(1/(2.*np.array(duration_cuts))/dT)  # Hz
    if np.max(duration_cuts) >= 1e6:
        freq_cuts[freq_cuts == np.min(freq_cuts)] = 0
    if verbose:
        print(f"In total: {len(freq_cuts)} frequency cuts have been created")
    return freq_cuts
