
def ensure_dtype_objs(
    dtype: DtypeArg | dict[Hashable, DtypeArg] | None,
) -> DtypeObj | dict[Hashable, DtypeObj] | None:
    """
    Ensure we have either None, a dtype object, or a dictionary mapping to
    dtype objects.
    """
    if isinstance(dtype, defaultdict):
        # "None" not callable  [misc]
        default_dtype = pandas_dtype(dtype.default_factory())  # type: ignore[misc]
        dtype_converted: defaultdict = defaultdict(lambda: default_dtype)
        for key in dtype.keys():
            dtype_converted[key] = pandas_dtype(dtype[key])
        return dtype_converted
    elif isinstance(dtype, dict):
        return {k: pandas_dtype(dtype[k]) for k in dtype}
    elif dtype is not None:
        return pandas_dtype(dtype)
    return dtype

