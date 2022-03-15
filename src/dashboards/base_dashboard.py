import ipywidgets as widgets
from IPython.display import display, clear_output

from src.helpers import Expando, detect_none_string
from src.helpers.fft import DURATION_CUTS


class DashboardBaseClass(object):
    """ This class is meant to be the base class for various dashboards based on the Fourier Decomposition df. """
    def __init__(self, data_frame):

        self.data_frame = data_frame

        _cols = self.data_frame.columns
        self.regions = list(sorted(_cols.get_level_values('region').unique()))
        self.variables = list(sorted(_cols.get_level_values('variable').unique()))

        # Lets keep the order of DURATION_CUTS
        _spectra = _cols.get_level_values('spectrum').unique()
        self.spectra = [
                           i for i in DURATION_CUTS.keys() if i in _spectra
                       ] + [
                           i for i in _spectra if i not in DURATION_CUTS.keys()
                       ]

        self.output = widgets.Output()

        # controls are VBoxes and HBoxes that will be displayed
        self.controls = Expando()
        self.controls.selection = None
        self.controls.buttons = None

        # widgets are individual widget elements
        self.widgets = Expando()
        self.widgets.regions = None
        self.widgets.variables = None
        self.widgets.spectra = None
        self.widgets.facet_row = None
        self.widgets.facet_col = None
        self.widgets.color = None
        self.widgets.line_dash = None

        # settings for plotly figure
        self.fig_regions = None
        self.fig_variables = None
        self.fig_spectra = None
        self.fig_facet_row = None
        self.fig_facet_col = None
        self.fig_color = None
        self.fig_line_dash = None
        self.fig_line_dash_map = None
        self.fig_cat_order = None

        self.set_generic_control_widgets()

    def set_specific_control_widgets(self):
        """Placeholder method for child classes."""
        pass

    def set_generic_control_widgets(self):
        """ Initializes all control widgets. """
        r = 'DE00' if 'DE00' in self.regions else self.regions[0]
        self.widgets.regions = widgets.SelectMultiple(description='Regions:', options=self.regions, value=[r], disabled=False)
        v = 'RES_sum' if 'RES_sum' in self.variables else self.variables[0]
        self.widgets.variables = widgets.SelectMultiple(description='Variables:', options=self.variables, value=[v], disabled=False)
        s = self.spectra[0]
        self.widgets.spectra = widgets.SelectMultiple(description='Spectra:', options=self.spectra, value=[s], disabled=False)

        _fig_grid = ['none', 'spectrum', 'region', 'variable']
        self.widgets.facet_row = widgets.Dropdown(options=_fig_grid, value='spectrum', description='Rows:', disabled=False)
        self.widgets.facet_col = widgets.Dropdown(options=_fig_grid, value='region', description='Columns:', disabled=False)
        self.widgets.color = widgets.Dropdown(options=_fig_grid, value='variable', description='Color:', disabled=False)
        self.widgets.line_dash = widgets.Dropdown(options=['confidence interval']+_fig_grid, value='none', description='Line dash:', disabled=False)

        _sel = widgets.HBox([self.widgets.regions, self.widgets.variables, self.widgets.spectra])
        _opt = widgets.HBox([self.widgets.facet_row, self.widgets.facet_col, self.widgets.color, self.widgets.line_dash])
        self.controls.selection = widgets.VBox([_sel, _opt])
        self.widgets.run_plot = widgets.Button(description="Create Plot")
        self.widgets.run_plot.on_click(self._create_plot)
        self.controls.buttons = widgets.HBox([self.widgets.run_plot])

    def _create_plot(self, _):
        self._load_figure_settings()
        with self.output:
            clear_output(wait=True)
            print("Creation of the plots...")
            clear_output(wait=True)
            self._specific_plot_from_interact()

    def _load_figure_settings(self):
        self.fig_regions = self.widgets.regions.value
        self.fig_variables = self.widgets.variables.value
        self.fig_spectra = self.widgets.spectra.value

        self.fig_facet_row = detect_none_string(self.widgets.facet_row.value)
        self.fig_facet_col = detect_none_string(self.widgets.facet_col.value)
        self.fig_color = detect_none_string(self.widgets.color.value)
        self.fig_line_dash = detect_none_string(self.widgets.line_dash.value)
        if self.fig_line_dash == 'confidence interval':
            self.fig_line_dash_map = {'upper_ci': 'dot', 'mean': 'solid', 'lower_ci': 'dot'}
        else:
            self.fig_line_dash_map = None

    def _specific_plot_from_interact(self):
        print('This function is defined in a child class.')
        pass

    def interact(self):
        display(self.controls.selection)
        display(self.controls.buttons)
        display(self.output)
