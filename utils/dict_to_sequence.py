from typing import Any

def dict_to_sequence(
    d: _t.SupportsItems[Any, Any] | Iterable[tuple[Any, Any]],
) -> Iterable[tuple[Any, Any]]:
    """Returns an internal sequence dictionary update."""

    if isinstance(d, _SupportsItems):
        return d.items()

    return d


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""

    if hasattr(d, "items"):
        d = d.items()

    return d

