
def _ensure_nanosecond_dtype(dtype: DtypeObj) -> None:
    """
    Convert dtypes with granularity less than nanosecond to nanosecond

    >>> _ensure_nanosecond_dtype(np.dtype("M8[us]"))

    >>> _ensure_nanosecond_dtype(np.dtype("M8[D]"))
    Traceback (most recent call last):
        ...
    TypeError: dtype=datetime64[D] is not supported. Supported resolutions are 's', 'ms', 'us', and 'ns'

    >>> _ensure_nanosecond_dtype(np.dtype("m8[ps]"))
    Traceback (most recent call last):
        ...
    TypeError: dtype=timedelta64[ps] is not supported. Supported resolutions are 's', 'ms', 'us', and 'ns'
    """  # noqa: E501
    msg = (
        f"The '{dtype.name}' dtype has no unit. "
        f"Please pass in '{dtype.name}[ns]' instead."
    )

    # unpack e.g. SparseDtype
    dtype = getattr(dtype, "subtype", dtype)

    if not isinstance(dtype, np.dtype):
        # i.e. datetime64tz
        pass

    elif dtype.kind in "mM":
        if not is_supported_dtype(dtype):
            # pre-2.0 we would silently swap in nanos for lower-resolutions,
            #  raise for above-nano resolutions
            if dtype.name in ["datetime64", "timedelta64"]:
                raise ValueError(msg)
            # TODO: ValueError or TypeError? existing test
            #  test_constructor_generic_timestamp_bad_frequency expects TypeError
            raise TypeError(
                f"dtype={dtype} is not supported. Supported resolutions are 's', "
                "'ms', 'us', and 'ns'"
            )

