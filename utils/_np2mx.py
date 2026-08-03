from typing import Dict

def _np2mx(numpy_dict: Dict[str, np.ndarray]) -> Dict[str, mx.array]:
    for k, v in numpy_dict.items():
        numpy_dict[k] = mx.array(v)
    return numpy_dict

