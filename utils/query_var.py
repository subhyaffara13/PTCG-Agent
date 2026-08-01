
def query_var(v: SimpleQuery) -> str:
    """Convert a query variable to a string.

    Note: Objects implementing the ``__int__`` data model method (typed as
    ``SupportsInt``; e.g. ``uuid.UUID``) are converted via ``int()`` first.
    Callers should convert such values to ``str`` explicitly if the string
    representation is desired.
    """
    cls = type(v)
    if cls is int:  # Fast path for non-subclassed int
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, float):
        if math.isinf(v):
            raise ValueError("float('inf') is not supported")
        if math.isnan(v):
            raise ValueError("float('nan') is not supported")
        return str(float(v))
    if cls is not bool and isinstance(v, SupportsInt):
        return str(int(v))
    raise TypeError(
        "Invalid variable type: value "
        "should be str, int or float, got {!r} "
        "of type {}".format(v, cls)
    )

