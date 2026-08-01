
def _is_valid_legacy_labelname(l: str) -> bool:
    """Returns true if the provided label name conforms to the legacy validation scheme."""
    if len(l) == 0:
        return False
    if METRIC_LABEL_NAME_RE.match(l) is None:
        return False
    return RESERVED_METRIC_LABEL_NAME_RE.match(l) is None

