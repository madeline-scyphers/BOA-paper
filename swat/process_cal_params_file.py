from pathlib import Path
import sys
from ruamel.yaml import YAML

cal_params_f = Path(__file__).parent / "TxtInOut/cal_parms.cal"

params = {}
with open(cal_params_f) as f:
    for i, line in enumerate(f):
        if i < 3:
            continue
        name1, name2, abs_min, abs_max, unit = line.split()
        name = f"{name1}.{name2}"
        params[name] = {
            "type": "range",
            "bounds": [float(abs_min), float(abs_max)],
            "value_type": "float"
        }

yaml = YAML()
yaml.indent(mapping=4, sequence=6, offset=3)
yaml.dump(params, sys.stdout)

print(len(params))