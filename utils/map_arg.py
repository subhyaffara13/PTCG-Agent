from typing import Any, Callable

def map_arg(a: ArgumentT, fn: Callable[[Node], Argument]) -> ArgumentT:
    """
    Apply fn recursively to each Node appearing in arg.

    arg may be a list, tuple, slice, or dict with string keys: the return value will
    have the same type and structure.
    """
    if not callable(fn):
        raise AssertionError("torch.fx.map_arg(a, fn): fn must be a callable")
    return _fx_map_arg(a, fn)


def map_arg(a: Any, fn: Callable[[Node], Any]) -> Any:
    return map_aggregate(a, lambda x: fn(x) if isinstance(x, Node) else x)

