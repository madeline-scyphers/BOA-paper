from ax.plot.feature_importances import plot_feature_importance_by_feature_plotly
from ax.service.utils.report_utils import FEATURE_IMPORTANCE_CAPTION
from ax.modelbridge.torch import TorchModelBridge
from ax.utils.sensitivity.sobol_measures import ax_parameter_sens
import panel as pn

from boa.plotting import _maybe_load_scheduler, SchedulerOrPath


def plot_feature_importance(scheduler: SchedulerOrPath):
    scheduler = _maybe_load_scheduler(scheduler)
    model = scheduler.model

    fig = plot_feature_importance_by_feature_plotly(model)
    return pn.pane.Plotly(fig)


def plot_feature_importance2(scheduler: SchedulerOrPath):
    scheduler = _maybe_load_scheduler(scheduler)
    model = scheduler.model
    importance_measure = ""
    sens=None

    try:
        sens = ax_parameter_sens(model, order="total")
        importance_measure = (
            '<a href="https://en.wikipedia.org/wiki/Variance-based_'
            'sensitivity_analysis">Variance-based sensitivity analysis</a>'
        )
    except NotImplementedError as e:
        print(f"Failed to compute global feature sensitivities: {e}")
    fig = plot_feature_importance_by_feature_plotly(
        model=model,
        # pyre-ignore [6]: In call for argument `sensitivity_values`,
        # expected `Optional[Dict[str, Dict[str, Union[float, ndarray]]]]`
        # but got `Dict[str, Dict[str, ndarray]]`.
        sensitivity_values=sens,
        relative=False,
        caption=FEATURE_IMPORTANCE_CAPTION if importance_measure == "" else "",
        importance_measure=importance_measure,
    )

    return pn.pane.Plotly(fig)
