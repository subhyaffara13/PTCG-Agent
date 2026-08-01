
def maybe_extract_name(name, obj, cls) -> Hashable:
    """
    If no name is passed, then extract it from data, validating hashability.
    """
    if name is None and isinstance(obj, (Index, ABCSeries)):
        # Note we don't just check for "name" attribute since that would
        #  pick up e.g. dtype.name
        name = obj.name

    # GH#29069
    if not is_hashable(name):
        raise TypeError(f"{cls.__name__}.name must be a hashable type")

    return name

