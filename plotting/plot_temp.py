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
from boa.plotting import app_view, _maybe_load_scheduler, plot_metrics_trace, plot_slice, plot_contours, scheduler_to_df

from pareto import plot_pareto


@click.command(
    epilog=f"Name of Plots to be added here: {', '.join(plot for plot in boa.plotting.__all__ if plot != 'app_view')}"
)
@click.option(
    "-sp",
    "--scheduler-path",
    type=click.Path(),
    default="",
    help="Path to scheduler json file.",
)
def main(scheduler_path):
    """
    Launch a basic EDA plot view of your optimization.
    Creating a web app with the scheduler json file.

    """
    scheduler = _maybe_load_scheduler(scheduler_path)
    view = pn.Column()
    if scheduler.experiment.is_moo_problem:
        pareto = plot_pareto(scheduler_path)
    else:
        pareto = None
    row1 = pn.Row(plot_metrics_trace(schedulers=scheduler))
    if pareto:
        row1.append(pareto)
    view.append(row1)
    view.append(plot_slice(scheduler=scheduler))
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
