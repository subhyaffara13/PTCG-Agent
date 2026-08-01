
def is_nested_object(obj) -> bool:
    """
    return a boolean if we have a nested object, e.g. a Series with 1 or
    more Series elements

    This may not be necessarily be performant.

    """
    return bool(
        isinstance(obj, ABCSeries)
        and is_object_dtype(obj.dtype)
        and any(isinstance(v, ABCSeries) for v in obj._values)
    )

