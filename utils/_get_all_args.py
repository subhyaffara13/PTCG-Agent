from typing import Any

def _get_all_args(
    args: Iterable[Any], kwargs: dict[str, Any]
) -> Iterable[VariableTracker]:
    return _flatten_vts(pytree.arg_tree_leaves(*args, **kwargs))

