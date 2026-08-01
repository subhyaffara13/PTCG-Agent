
def _validate_metric_name(name: str) -> None:
    """Raises ValueError if the provided name is not a valid metric name.
    
    This check uses the global legacy validation setting to determine the validation scheme.
    """
    if not name:
        raise ValueError("metric name cannot be empty")
    if _legacy_validation:
        if not METRIC_NAME_RE.match(name):
            raise ValueError("invalid metric name " + name)
    try:
        name.encode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("invalid metric name " + name)

