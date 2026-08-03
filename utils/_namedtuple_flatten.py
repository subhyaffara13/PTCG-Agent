from typing import Any

def _namedtuple_flatten(d: NamedTuple) -> tuple[list[Any], Context]:
    return list(d), type(d)

