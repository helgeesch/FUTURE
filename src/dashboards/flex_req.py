import numpy as np
import plotly.express as px

from src.helpers import datetime_index_to_hour_of_year, upper_ci, lower_ci
from .base_dashboard import DashboardBaseClass

DEFAULT_PERCENTILES = list(range(0, 80, 5)) + list(range(80, 101, 1))


def percentile_func(percentile):
    filtr = lambda x: np.where(x <= 0, x, np.nan)
    perc = lambda x: np.nanpercentile(np.abs(filtr(x)), percentile)
    return perc


class FlexibilityRequirementDashboard(DashboardBaseClass):
    def __init__(self, data_frame):
        super().__init__(data_frame)

    def _specific_plot_from_interact(self):
        _regions = self.fig_regions
        _variables = self.fig_variables
        _spectra = self.fig_spectra
        _facet_row = self.fig_facet_row
        _facet_col = self.fig_facet_col
        _color = self.fig_color
        _line_dash = self.fig_line_dash
        _line_dash_map = self.fig_line_dash_map

        if _line_dash == 'confidence interval':
            agg = [upper_ci, 'mean', lower_ci]
            print('# NOTE: You chose to show the confidence intervals, this significantly increases plot-time. '
                  'Please be prepared to wait a couple of minutes. :)')
            _line_dash = 'aggregation'
        else:
            agg = ['mean']

        # FLEX REQ DATA prep
        data = self.data_frame.loc(axis=1)[_regions, _variables, _spectra]
        data = datetime_index_to_hour_of_year(data)
        _cols = data.columns.names
        _percentile_aggregation = [(p, percentile_func(p)) for p in DEFAULT_PERCENTILES]
        data = data.groupby(level='year', axis=0).agg(_percentile_aggregation)
        data.columns.names = _cols + ['percentile']
        data = data.stack('percentile')
        _cols = data.columns.names
        data = data.groupby(level='percentile', axis=0).agg(agg)
        data.columns.names = _cols + ['aggregation']

        # PLOT
        cat_order = {'spectrum': _spectra}
        if _line_dash == 'aggregation':
            cat_order.update({'aggregation': ['upper_ci', 'mean', 'lower_ci']})

        plot_df = (data / 1e3).round(2).reset_index().melt(id_vars='percentile').sort_values('percentile')
        num_rows = len(plot_df[_facet_row].unique()) if _facet_row is not None else 1
        fig = px.line(
            plot_df,
            x='percentile',
            y='value',
            line_dash=_line_dash,
            color=_color,
            facet_row=_facet_row,
            facet_col=_facet_col,
            labels={'value': 'flex requirements [GW]'},
            category_orders=cat_order,
            line_dash_map=_line_dash_map,
            height=350 * num_rows + 150,
        )
        fig.update_layout(
            title_text=f'<b>Upward Flexibility Requirements</b>',
            title_x=0.5,
        )
        fig.show()
