
def _is_valid_legacy_metric_name(name: str) -> bool:
    """Returns true if the provided metric name conforms to the legacy validation scheme."""
    if len(name) == 0:
        return False
    return METRIC_NAME_RE.match(name) is not None

