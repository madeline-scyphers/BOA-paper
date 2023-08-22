from __future__ import annotations

from ax.core.base_trial import TrialStatus
from dataclasses import dataclass, field
import collections
from typing import Optional, Sequence, Any

import plotly.graph_objs as go
import json
import enum
import panel as pn
import numpy as np

from boa.plotting import _maybe_load_scheduler, SchedulerOrPath


def plot_pareto(scheduler: SchedulerOrPath):
    scheduler = _maybe_load_scheduler(scheduler)
    experiment = scheduler.experiment
    ax_objectives = experiment.optimization_config.objective.objectives
    trials = experiment.trials_by_status[TrialStatus.COMPLETED]
    metric_names = [obj.metric.name for obj in ax_objectives]
    directions = []
    for obj in ax_objectives:
        if obj.metric.name in metric_names:
            directions.append(
                StudyDirection(StudyDirection.MINIMIZE) if obj.minimize else StudyDirection(StudyDirection.MAXIMIZE))
    trials_data = []

    trials.sort(key=lambda trial: trial.index)
    for trial in trials:
        data = trial.fetch_data()
        trials_data.append(data.df.loc[data.df.metric_name.isin(metric_names)]["mean"].values)

    best_trials = _get_pareto_front_trials_by_trials(trials_data, directions)
    non_best_trials = _get_non_pareto_front_trials(trials_data, best_trials)
    print(f"n total trials: {len(trials_data)}, n pareto trials: {len(best_trials)}")

    metric_names = metric_names
    n_targets = len(metric_names)
    axis_order = list(range(n_targets))

    info = ParetoFrontInfo(
        n_targets=n_targets,
        target_names=metric_names,
        # best_trials_with_values=_make_trials_with_values(best_trials),
        best_trials_with_values=best_trials,
        # non_best_trials_with_values=_make_trials_with_values(non_best_trials),
        non_best_trials_with_values=non_best_trials,
        infeasible_trials_with_values=[],
        axis_order=axis_order,
        include_dominated_trials=True,
        has_constraints_func=False
    )
    return pn.pane.Plotly(get_pareto_front_plot(info))



@dataclass
class ParetoFrontInfo:
    n_targets: int
    target_names: list[str]
    best_trials_with_values: list
    non_best_trials_with_values: list
    infeasible_trials_with_values: field(default_factory=list)
    axis_order: list[int]
    include_dominated_trials: bool
    has_constraints_func: bool


class StudyDirection(enum.IntEnum):
    """Direction of a :class:`~optuna.study.Study`.

    Attributes:
        NOT_SET:
            Direction has not been set.
        MINIMIZE:
            :class:`~optuna.study.Study` minimizes the objective function.
        MAXIMIZE:
            :class:`~optuna.study.Study` maximizes the objective function.
    """

    NOT_SET = 0
    MINIMIZE = 1
    MAXIMIZE = 2


def _get_pareto_front_trials_by_trials(
    trials, directions
):
    if len(directions) == 2:
        return _get_pareto_front_trials_2d(trials, directions)  # Log-linear in number of trials.
    return _get_pareto_front_trials_nd(trials, directions)  # Quadratic in number of trials.


def _get_pareto_front_trials_2d(
        trials, directions
):
    n_trials = len(trials)
    if n_trials == 0:
        return []

    trials.sort(
        key=lambda trial: (
            _normalize_value(trial[0], directions[0]),
            _normalize_value(trial[1], directions[1]),
        ),
    )

    last_nondominated_trial = trials[0]
    pareto_front = [last_nondominated_trial]
    for i in range(1, n_trials):
        trial = trials[i]
        if _dominates(last_nondominated_trial, trial, directions):
            continue
        pareto_front.append(trial)
        last_nondominated_trial = trial

    pareto_front
    return pareto_front


def _get_pareto_front_trials_nd(
        trials, directions
):
    pareto_front = []

    # TODO(vincent): Optimize (use the fast non dominated sort defined in the NSGA-II paper).
    for trial in trials:
        dominated = False
        for other in trials:
            if _dominates(other, trial, directions):
                dominated = True
                break

        if not dominated:
            pareto_front.append(trial)

    return pareto_front


def _dominates(
        trial0, trial1, directions
) -> bool:
    values0 = trial0
    values1 = trial1
    # values0 = trial0.fetch_data().df["mean"]
    # values1 = trial1.fetch_data().df["mean"]

    assert values0 is not None
    assert values1 is not None

    if len(values0) != len(values1):
        raise ValueError("Trials with different numbers of objectives cannot be compared.")

    if len(values0) != len(directions):
        raise ValueError(
            "The number of the values and the number of the objectives are mismatched."
        )

    normalized_values0 = [_normalize_value(v, d) for v, d in zip(values0, directions)]
    normalized_values1 = [_normalize_value(v, d) for v, d in zip(values1, directions)]

    if normalized_values0 == normalized_values1:
        return False

    return all(v0 <= v1 for v0, v1 in zip(normalized_values0, normalized_values1))


def _normalize_value(value: Optional[float], direction: StudyDirection) -> float:
    if value is None:
        value = float("inf")

    if direction is StudyDirection.MAXIMIZE:
        value = -value

    return value


def _get_non_pareto_front_trials(
    trials, pareto_trials
):
    non_pareto_trials = []
    for trial in trials:
        if not arrayisin(trial, pareto_trials):
            non_pareto_trials.append(trial)
    return non_pareto_trials


def arrayisin(array, list_of_arrays):
    for a in list_of_arrays:
        if np.array_equal(array, a):
            return True
    return False

def _make_scatter_object(
    n_targets: int,
    axis_order: Sequence[int],
    include_dominated_trials: bool,
    trials_with_values,
    hovertemplate: str,
    infeasible: bool = False,
    dominated_trials: bool = False,
) -> "go.Scatter" | "go.Scatter3d":
    trials_with_values = trials_with_values or []

    marker = _make_marker(
        [trial for trial in trials_with_values],
        include_dominated_trials,
        dominated_trials=dominated_trials,
        infeasible=infeasible,
    )
    if n_targets == 2:
        return go.Scatter(
            x=[values[axis_order[0]] for values in trials_with_values],
            y=[values[axis_order[1]] for values in trials_with_values],
            # text=[_make_hovertext(trial) for trial, _ in trials_with_values],
            mode="markers",
            hovertemplate=hovertemplate,
            marker=marker,
            showlegend=False,
        )
    elif n_targets == 3:
        return go.Scatter3d(
            x=[values[axis_order[0]] for values in trials_with_values],
            y=[values[axis_order[1]] for values in trials_with_values],
            z=[values[axis_order[2]] for values in trials_with_values],
            # text=[_make_hovertext(trial) for trial, _ in trials_with_values],
            mode="markers",
            hovertemplate=hovertemplate,
            marker=marker,
            showlegend=False,
        )
    else:
        assert False, "Must not reach here"


def _make_marker(
    trials,
    include_dominated_trials: bool,
    dominated_trials: bool = False,
    infeasible: bool = False,
) -> dict[str, Any]:
    if dominated_trials and not include_dominated_trials:
        assert len(trials) == 0

    if infeasible:
        return {
            "color": "#cccccc",
        }
    elif dominated_trials:
        return {
            "line": {"width": 0.5, "color": "Grey"},
            "color": [idx for idx in range(len(trials))],
            "color": "black",
            "symbol": "diamond",
            "size": 10
        }
    else:
        return {
            "line": {"width": 0.5, "color": "Grey"},
            "color": [idx for idx in range(len(trials))],
            "colorscale": "viridis",
            "size": 10,
            "colorbar": {
                "title": "Pareto Front",
                # "x": 1.1 if include_dominated_trials else 1,
                # "xpad": 40,
            },
        }

def get_pareto_front_plot(info: ParetoFrontInfo) -> "go.Figure":
    include_dominated_trials = info.include_dominated_trials
    has_constraints_func = info.has_constraints_func
    if not has_constraints_func:
        data = [
            _make_scatter_object(
                info.n_targets,
                info.axis_order,
                include_dominated_trials,
                info.non_best_trials_with_values,
                hovertemplate="%{text}<extra>Other Points</extra>",
                dominated_trials=True,
            ),
            _make_scatter_object(
                info.n_targets,
                info.axis_order,
                include_dominated_trials,
                info.best_trials_with_values,
                hovertemplate="%{text}<extra>Pareto Front Points</extra>",
                dominated_trials=False,
            ),
        ]
    else:
        data = [
            _make_scatter_object(
                info.n_targets,
                info.axis_order,
                include_dominated_trials,
                info.infeasible_trials_with_values,
                hovertemplate="%{text}<extra>Infeasible Trial</extra>",
                infeasible=True,
            ),
            _make_scatter_object(
                info.n_targets,
                info.axis_order,
                include_dominated_trials,
                info.non_best_trials_with_values,
                hovertemplate="%{text}<extra>Feasible Trial</extra>",
                dominated_trials=True,
            ),
            _make_scatter_object(
                info.n_targets,
                info.axis_order,
                include_dominated_trials,
                info.best_trials_with_values,
                hovertemplate="%{text}<extra>Pareto Front Points</extra>",
                dominated_trials=False,
            ),
        ]

    if info.n_targets == 2:
        layout = go.Layout(
            title="Pareto Front",
            xaxis_title=info.target_names[info.axis_order[0]],
            yaxis_title=info.target_names[info.axis_order[1]],
        )
    else:
        layout = go.Layout(
            title="Pareto Front",
            scene={
                "xaxis_title": info.target_names[info.axis_order[0]],
                "yaxis_title": info.target_names[info.axis_order[1]],
                "zaxis_title": info.target_names[info.axis_order[2]],
            },
        )
    return go.Figure(data=data, layout=layout)
