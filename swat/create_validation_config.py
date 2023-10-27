import click
import pandas as pd
from pathlib import Path
import boa
import copy
import json

METRIC_NAME = "flo_out_NSE"


@click.command()
@click.option(
    "-o",
    "--optimization-path",
    type=click.Path(exists=True, dir_okay=True, path_type=Path),
    help="Path to BOA optimization folder.",
)
@click.option(
    "-c",
    "--config-path",
    type=click.Path(path_type=Path),
    help="Path to original config file.",
)
def main(optimization_path, config_path):
    df = pd.read_csv(optimization_path / "optimization.csv")
    best_cal = df.loc[df[METRIC_NAME] == df[METRIC_NAME].max()]
    if not config_path:
        config_path = optimization_path / "config.yaml"
    config_orig = boa.load_jsonlike(config_path)
    parameters = {}
    config = {
        "objective": copy.deepcopy(config_orig["objective"]),
        "scheduler": {"n_trials": 1},
        "script_options": copy.deepcopy(config_orig["script_options"]),
        "parameters": {}
        }
    for parameter, d in config_orig["parameters"].items():
        if d["type"] == "range":
            val = best_cal[parameter].iloc[0]
            config["parameters"][parameter] = {
                "value": val,
                "type": "fixed"
            }
            parameters[parameter] = val
    config["parameters"]["start_date"] = {"type": "fixed",
                                          "value": "2018-01-01"}
    parameters["start_date"] = "2018-01-01"
    config["parameters"]["end_date"] = {"type": "fixed",
                                        "value": "2021-01-01"}
    parameters["end_date"] = "2021-01-01"
    config["parameters"]["years_skip"] = {"type": "fixed",
                                          "value": 0}
    parameters["years_skip"] = 0

    validation_p = optimization_path / "validation"
    validation_p.mkdir(exist_ok=True)

    with open(validation_p / "config.json", "w") as f:
        json.dump(config, f, indent=4)
    with open(validation_p / "parameters.json", "w") as f:
        json.dump(parameters, f, indent=4)

    print(f"Best validation trial so far: {best_cal['trial_index']=}")
    print(f"Beat metric for that trial: {best_cal[METRIC_NAME]=}")


if __name__ == "__main__":
    main()
