from ax.modelbridge.modelbridge_utils import observed_hypervolume, predicted_hypervolume, hypervolume
from ax.core.base_trial import TrialStatus
from ax.modelbridge.factory import get_MOO_EHVI
import plotly.express as px
import numpy as np
import panel as pn

from boa.plotting import _maybe_load_scheduler, SchedulerOrPath


pn.extension('plotly')


def plot_hypervolume(scheduler: SchedulerOrPath):
    scheduler = _maybe_load_scheduler(scheduler)
    experiment = scheduler.experiment
    model = scheduler.generation_strategy.model

    hvs = []
    for i in range(1, len(experiment.trials_by_status[TrialStatus.COMPLETED]) + 1):
        dummy_model = get_MOO_EHVI(
            experiment=experiment,
            data=experiment.fetch_trials_data(np.arange(i)),
            search_space=experiment.search_space,
            optimization_config=experiment.optimization_config,
        )
        hvs.append(observed_hypervolume(
            modelbridge=dummy_model,
            objective_thresholds=experiment.optimization_config.objective_thresholds or model.infer_objective_thresholds
        ))
    log_hv = np.asarray(hvs)
    fig = px.line(x=np.arange(len(hvs)), y=log_hv, title='HyperVolume')
    return pn.pane.Plotly(fig)
