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

    def fetch_trial_data(self, parameters, param_names, metric_name, **kwargs):

        res = f([param for name, param in parameters.items() if name in param_names])
        return {
            f"obj{i}": float(res[i]) for i in range(n_obj)
        }
        # return {"a": f_a([param for name, param in parameters.items() if name in self.metric_params["a"]]),
        #         "b": f_b([param for name, param in parameters.items() if name in self.metric_params["b"]])}
        #
        # return {"a": f1(list(parameters.values())), "b": f2(list(parameters.values()))}


def f(x):
    return problem(torch.tensor(x, **tkwargs).clamp(0.0, 1.0))


def f_a(x) -> float:
    return float(problem(torch.tensor(x, **tkwargs).clamp(0.0, 1.0))[0])


def f_b(x) -> float:
    return float(problem(torch.tensor(x, **tkwargs).clamp(0.0, 1.0))[1])
