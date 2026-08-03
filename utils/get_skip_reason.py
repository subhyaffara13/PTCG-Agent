from typing import Any

def get_skip_reason(obj: Any) -> str:
    """Compute a descriptive skip reason for a callable. Only called on graph break."""
    if is_callable_disallowed(obj):
        return _disallowed_callable_ids.get_name(id(obj), repr(obj))

    filename = getfile(obj)
    if filename is not None:
        skip_result = check_file(filename)
        if skip_result.reason is not None:
            return skip_result.reason

    module = getattr(obj, "__module__", None) or ""
    return (
        f"cannot determine source file for {module} (likely a C extension or builtin)"
    )

