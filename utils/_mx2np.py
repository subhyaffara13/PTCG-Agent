from typing import Dict

def _mx2np(mx_dict: Dict[str, mx.array]) -> Dict[str, np.array]:
    new_dict = {}
    for k, v in mx_dict.items():
        new_dict[k] = np.asarray(v)
    return new_dict

