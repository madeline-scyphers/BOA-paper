import numpy as np

from boa import BaseWrapper

class WrapperSaasbo(BaseWrapper):
    def run_model(self, trial) -> None:
        pass

    def set_trial_status(self, trial) -> None:
        trial.mark_completed()

    def fetch_trial_data(self, parameters, param_names=None, **kwargs):
        parameters = np.array([v for k, v in parameters.items() if k in param_names])
        return {"branin": parameters}
