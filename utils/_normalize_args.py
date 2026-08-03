from typing import Any

def _normalize_args(
    node: Node,
) -> tuple[tuple[str, ...], tuple[Any | None, ...]]:
    flat_args, _ = tree_flatten(node.args)
    sorted_kwargs = sorted(node.kwargs.items(), key=operator.itemgetter(0))
    sorted_keys = tuple(sorted(node.kwargs.keys()))
    flat_kwargs, _ = tree_flatten(sorted_kwargs)
    all_args = flat_args + flat_kwargs
    return (sorted_keys, tuple(_extract_args(arg) for arg in all_args))

