
def _normalize_property_name(string):
    """Remove case, strip space, '-' and '_' for loose matching."""
    return _normalize_re.sub("", string).lower()

