
def is_empty_slice(obj) -> bool:
    """
    We have an empty slice, e.g. no values are selected.
    """
    return (
        isinstance(obj, slice)
        and obj.start is not None
        and obj.stop is not None
        and obj.start == obj.stop
    )

