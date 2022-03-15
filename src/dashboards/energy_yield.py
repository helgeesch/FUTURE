import ipywidgets as widgets
import plotly.express as px
from plotly.subplots import make_subplots

from .base_dashboard import DashboardBaseClass


class EnergyYieldDashboard(DashboardBaseClass):
    def __init__(self, data_frame):
        super().__init__(data_frame)
        self.widgets.groupby = None
        self.set_specific_control_widgets()

    def set_specific_control_widgets(self):
        self.widgets.variables.default_value = ['pv', 'onshore', 'offshore']
        self.widgets.variables.value = self.widgets.variables.default_value
        self.widgets.groupby = widgets.RadioButtons(
            options=['region', 'variable'],
            value='region',
            layout={'width': 'max-content'},
            description='Group by',
            disabled=False,
        )
        _sel = widgets.HBox([self.widgets.regions, self.widgets.variables, self.widgets.groupby])
        self.controls.selection = _sel

    def _specific_plot_from_interact(self):
        _regions = self.fig_regions
        _variables = self.fig_variables
        _groupby = self.widgets.groupby.value

        data = self.data_frame.loc(axis=1)[_regions, _variables, 'raw_data']
        groups = data.columns.get_level_values(_groupby).unique()
        num_groups = len(groups)
        fig = make_subplots(rows=1, cols=num_groups,
                            specs=[[{'type': 'domain'}]*num_groups],
                            subplot_titles=[g for g in groups]
                            )
        for i, g in enumerate(groups):
            mask = data.columns.get_level_values(_groupby) == g
            plot_df = (data.loc(axis=1)[mask].sum() / 1e6 / len(data) * 8760).round(2).to_frame('value').reset_index()
            _inv_groupby = 'variable' if _groupby == 'region' else 'region'
            fig_yield = px.pie(
                plot_df,
                values='value',
                names=_inv_groupby,
                labels={'value': 'annualized yield [TWh]'},
                color=_inv_groupby,
                color_discrete_map={'pv': 'yellow', 'onshore': 'royalblue', 'offshore': 'darkblue'},
            )
            fig_yield.update_layout(showlegend=False)
            fig.add_trace(fig_yield.data[0], row=1, col=1+i)
        fig.update_layout(title_text='<b>Energy Yield per Group</b>', title_x=0.5)
        fig.show()
