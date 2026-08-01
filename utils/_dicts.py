
def _dicts(value: object) -> tuple[Mapping[str, object], ...]:
    """The dict items of ``value`` (when it's a list), as a tuple. Else empty."""
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, dict))

