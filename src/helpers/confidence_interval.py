import numpy as np
import scipy.stats as st


def upper_ci(x):
    return st.t.interval(0.95, len(x) - 1, loc=np.mean(x), scale=st.sem(x))[1]


def lower_ci(x):
    return st.t.interval(0.95, len(x) - 1, loc=np.mean(x), scale=st.sem(x))[0]


upper_ci.__name__ = 'upper_ci'
lower_ci.__name__ = 'lower_ci'
