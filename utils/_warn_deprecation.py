from typing import Any, Dict

def _warn_deprecation(name: str, module_globals: Dict[str, Any]) -> Any:
    if (val := module_globals.get(f"_DEPRECATED_{name}")) is None:
        msg = f"module '{__name__}' has no attribute '{name}'"
        raise AttributeError(msg)
    module_globals[name] = val
    if name in {"NoReturn"}:
        msg = (
            f"'mypy_extensions.{name}' is deprecated, "
            "and will be removed in a future version. "
            f"Use 'typing.{name}' or 'typing_extensions.{name}' instead"
        )
    else:
        assert False, f"Add deprecation message for 'mypy_extensions.{name}'"
    import warnings
    warnings.warn(msg, DeprecationWarning, stacklevel=3)
    return val

