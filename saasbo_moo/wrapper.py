import torch

from boa import BaseWrapper, get_synth_func
from boa.utils import torch_device

n_obj = 2
d = 10
tkwargs = {
    "device": torch_device(),
}
synth_func = get_synth_func("DTLZ2")
problem = synth_func(num_objectives=n_obj, dim=d, negate=True).to(**tkwargs)


class WrapperSaasboMoo(BaseWrapper):
    def run_model(self, trial) -> None:
        pass

    def set_trial_status(self, trial) -> None:
        trial.mark_completed()

    def fetch_trial_data(self, parameters, **kwargs):
        return {"a": f1(list(parameters.values())), "b": f2(list(parameters.values()))}


def f1(x) -> float:
    return float(problem(torch.tensor(x, **tkwargs).clamp(0.0, 1.0))[0])


def f2(x) -> float:
    return float(problem(torch.tensor(x, **tkwargs).clamp(0.0, 1.0))[1])
