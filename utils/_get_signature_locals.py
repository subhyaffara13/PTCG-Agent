from typing import Any, Callable

def _get_signature_locals(f: Callable, loc: dict[str, Any]) -> dict[str, Any]:
    """Get local keyword arguments

    Example::

    >> def f(self, a, b=9):
           pass
    >> loc = {"a": 6, "c": 7}
    >> _get_signature_locals(f, loc)
    {"a": 6}
    """
    return {k: v for k, v in loc.items() if k in signature(f).parameters}

