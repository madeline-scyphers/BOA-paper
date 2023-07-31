import boa
import torch
from botorch.test_functions.multi_objective import DTLZ2

num_objs = 6
d = 8

tkwargs = {
    "dtype": torch.double,
    "device": boa.utils.torch_device(),
}
problem = DTLZ2(num_objectives=num_objs, dim=d, negate=True).to(**tkwargs)


class Wrapper(boa.BaseWrapper):
    def run_model(self, trial) -> None:
        pass

    def set_trial_status(self, trial) -> None:
        trial.mark_completed()

    def fetch_trial_data(self, trial, metric_properties, metric_name, *args, **kwargs):
        evaluation = problem(torch.tensor(*trial.arm.parameters.values()))
        return {i: float(obj) for i, obj in enumerate(evaluation)}
