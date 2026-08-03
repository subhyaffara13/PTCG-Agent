from typing import Any, Dict

def _build_sandbox_builtins() -> Dict[str, Any]:
    # ``limited_builtins`` overrides ``list``/``tuple``/``range`` from
    # ``safe_builtins`` with bounds-checking variants (e.g. ``limited_range``
    # rejects ``range(10**18)``). ``utility_builtins`` adds ``set``,
    # ``frozenset``, ``math``, ``random``, and a filtered ``string`` delegator.
    return {
        **safe_builtins,
        **limited_builtins,
        **utility_builtins,
    }

