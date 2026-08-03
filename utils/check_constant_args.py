import itertools
from typing import Any

def check_constant_args(args: Iterable[Any], kwargs: Mapping[Any, Any]) -> bool:
    return all(x.is_python_constant() for x in itertools.chain(args, kwargs.values()))

