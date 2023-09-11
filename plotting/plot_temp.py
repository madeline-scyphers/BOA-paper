"""
BOA plotting CLI module

You can launch a basic EDA plot view
of your optimization with::

    python -m boa.plot path/to/scheduler.json


"""


import pathlib

import click
import panel as pn

import boa.plotting
from boa.plotting import _maybe_load_scheduler, plot_metrics_trace, plot_slice, plot_contours, scheduler_to_df

from pareto import plot_pareto
from hypervolume import plot_hypervolume
# from feature_importance import plot_feature_importance, plot_feature_importance2


@click.command(
    epilog=f"Name of Plots to be added here: {', '.join(plot for plot in boa.plotting.__all__ if plot != 'get_plots')}"
)
@click.option(
    "-sp",
    "--scheduler-path",
    type=click.Path(),
    default="",
    help="Path to scheduler json file.",
)
@click.option(
    "-mhv",
    "--max-hypervolume",
    type=float,
    help="Maximum hypervolume value to be plotted against.",
)
def main(scheduler_path, max_hypervolume):
    """
    Launch a basic EDA plot view of your optimization.
    Creating a web app with the scheduler json file.

    """
    scheduler = _maybe_load_scheduler(scheduler_path)
    view = pn.Column()
    if scheduler.experiment.is_moo_problem:
        moo_plots = pn.Row(
            plot_pareto(scheduler),
            plot_hypervolume(scheduler, max_hypervolume=max_hypervolume)
        )

    else:
        moo_plots = None
    view.append(pn.Row(plot_metrics_trace(schedulers=scheduler)))
    if moo_plots:
        view.append(moo_plots)
    view.append(plot_slice(scheduler=scheduler))
    # view.append(plot_feature_importance(scheduler=scheduler))
    # view.append(plot_feature_importance2(scheduler=scheduler))
    view.append(plot_contours(scheduler=scheduler))
    view.append(scheduler_to_df(scheduler))

    template = pn.template.BootstrapTemplate(
        site="BOA",
        main=[view],
    )
    template.servable()
    pn.serve({pathlib.Path(__file__).name: template})


if __name__ == "__main__":
    main()
