import itertools
from typing import Any

def check_numpy_ndarray_args(args: Iterable[Any], kwargs: Mapping[Any, Any]) -> bool:
    from .variables.tensor import NumpyNdarrayVariable

    return any(
        isinstance(x, NumpyNdarrayVariable)
        for x in itertools.chain(args, kwargs.values())
    )

