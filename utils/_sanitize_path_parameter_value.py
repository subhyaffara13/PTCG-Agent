from typing import Any

def _sanitize_path_parameter_value(param_value: Any, param_name: str) -> str:
    """Ensure path params cannot introduce directory traversal."""
    if param_value is None:
        return ""

    value_str = str(param_value)
    if value_str == "":
        return ""

    normalized_value = value_str.replace("\\", "/")
    if "/" in normalized_value:
        raise ValueError(
            f"Path parameter '{param_name}' must not contain path separators"
        )

    if any(part in {".", ".."} for part in PurePosixPath(normalized_value).parts):
        raise ValueError(
            f"Path parameter '{param_name}' cannot include '.' or '..' segments"
        )

    return quote(value_str, safe="")

