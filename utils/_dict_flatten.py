from typing import Any

def _dict_flatten(d: dict[Any, T]) -> tuple[list[T], Context]:
    return list(d.values()), list(d.keys())

