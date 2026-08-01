
def astype_is_view(dtype: DtypeObj, new_dtype: DtypeObj) -> bool:
    """Checks if astype avoided copying the data.

    Parameters
    ----------
    dtype : Original dtype
    new_dtype : target dtype

    Returns
    -------
    True if new data is a view or not guaranteed to be a copy, False otherwise
    """
    if dtype.kind in "iufb" and dtype.kind == new_dtype.kind:
        # fastpath for numeric dtypes
        if hasattr(dtype, "itemsize") and hasattr(new_dtype, "itemsize"):
            return dtype.itemsize == new_dtype.itemsize  # pyright: ignore[reportAttributeAccessIssue]

    if isinstance(dtype, np.dtype) and not isinstance(new_dtype, np.dtype):
        new_dtype, dtype = dtype, new_dtype

    if dtype == new_dtype:
        return True

    elif isinstance(dtype, np.dtype) and isinstance(new_dtype, np.dtype):
        # Only equal numpy dtypes avoid a copy
        return False

    elif is_string_dtype(dtype) and is_string_dtype(new_dtype):
        from pandas.core.arrays.string_ import StringDtype

        if (
            isinstance(dtype, StringDtype)
            and dtype.storage == "pyarrow"
            and new_dtype == "object"
        ):
            # for conversion of pyarrow array to numpy object array -> always a copy
            return False
        # Potentially! a view when converting from object to string
        return True

    elif is_object_dtype(dtype) and new_dtype.kind == "O":
        # When the underlying array has dtype object, we don't have to make a copy
        return True

    elif dtype.kind in "mM" and new_dtype.kind in "mM":
        dtype = getattr(dtype, "numpy_dtype", dtype)
        new_dtype = getattr(new_dtype, "numpy_dtype", new_dtype)
        return getattr(dtype, "unit", None) == getattr(new_dtype, "unit", None)

    elif new_dtype == object and isinstance(
        dtype, (DatetimeTZDtype, PeriodDtype, IntervalDtype)
    ):
        return False

    elif isinstance(dtype, CategoricalDtype) and not isinstance(
        new_dtype, CategoricalDtype
    ):
        return False

    numpy_dtype = getattr(dtype, "numpy_dtype", None)
    new_numpy_dtype = getattr(new_dtype, "numpy_dtype", None)

    if numpy_dtype is None and isinstance(dtype, np.dtype):
        numpy_dtype = dtype

    if new_numpy_dtype is None and isinstance(new_dtype, np.dtype):
        new_numpy_dtype = new_dtype

    if numpy_dtype is not None and new_numpy_dtype is not None:
        # if both have NumPy dtype or one of them is a numpy dtype
        # they are only a view when the numpy dtypes are equal, e.g.
        # int64 -> Int64 or int64[pyarrow]
        # int64 -> Int32 copies
        return numpy_dtype == new_numpy_dtype

    # Assume this is a view since we don't know for sure if a copy was made
    return True

