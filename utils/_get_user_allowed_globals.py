from typing import Any

def _get_user_allowed_globals():
    rc: dict[str, Any] = {}
    for f in _marked_safe_globals_set:
        if isinstance(f, tuple):
            if len(f) != 2:
                raise ValueError(
                    f"Expected tuple of length 2 (global, str of callable full path), but got tuple of length: {len(f)}"
                )
            if type(f[1]) is not str:
                raise TypeError(
                    f"Expected second item in tuple to be str of callable full path, but got: {type(f[1])}"
                )
            f, name = f
            rc[name] = f
        else:
            module, name = f.__module__, f.__qualname__
            rc[f"{module}.{name}"] = f
    return rc

