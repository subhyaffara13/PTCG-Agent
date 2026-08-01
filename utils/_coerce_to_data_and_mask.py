
def _coerce_to_data_and_mask(values, dtype, copy: bool, dtype_cls: type[NumericDtype]):
    checker = dtype_cls._checker
    default_dtype = dtype_cls._default_np_dtype

    mask = None
    inferred_type = None

    if dtype is None and hasattr(values, "dtype"):
        if checker(values.dtype):
            dtype = values.dtype

    if dtype is not None:
        dtype = dtype_cls._standardize_dtype(dtype)

    cls = dtype_cls().construct_array_type()
    if isinstance(values, cls):
        values, mask = values._data, values._mask
        if dtype is not None:
            values = values.astype(dtype.numpy_dtype, copy=False)

        if copy:
            values = values.copy()
            mask = mask.copy()
        return values, mask

    original = values
    if not copy:
        values = np.asarray(values)
    else:
        values = np.array(values, copy=copy)
    inferred_type = None
    if values.dtype == object or is_string_dtype(values.dtype):
        inferred_type = lib.infer_dtype(values, skipna=True)
        if inferred_type == "boolean" and dtype is None:
            # object dtype array of bools
            name = dtype_cls.__name__.strip("_")
            raise TypeError(f"{values.dtype} cannot be converted to {name}")

    elif values.dtype.kind == "b" and checker(dtype):
        # fastpath
        mask = np.zeros(len(values), dtype=np.bool_)
        if not copy:
            values = np.asarray(values, dtype=default_dtype)
        else:
            values = np.array(values, dtype=default_dtype, copy=copy)

    elif values.dtype.kind not in "iuf":
        name = dtype_cls.__name__.strip("_")
        raise TypeError(f"{values.dtype} cannot be converted to {name}")

    if values.ndim != 1:
        raise TypeError("values must be a 1D list-like")

    if mask is None:
        if values.dtype.kind in "iu":
            # fastpath
            mask = np.zeros(len(values), dtype=np.bool_)
        elif values.dtype.kind == "f":
            # np.isnan is faster than is_numeric_na() for floats
            # github issue: #60066
            if is_nan_na():
                mask = np.isnan(values)
            else:
                mask = np.zeros(len(values), dtype=np.bool_)
                if dtype_cls.__name__.strip("_").startswith(("I", "U")):
                    wrong = np.isnan(values)
                    if wrong.any():
                        raise ValueError("Cannot cast NaN value to Integer dtype.")
        elif is_nan_na():
            mask = libmissing.is_numeric_na(values)
        else:
            # is_numeric_na will raise on non-numeric NAs
            libmissing.is_numeric_na(values)
            mask = libmissing.is_pdna_or_none(values)
    else:
        assert len(mask) == len(values)

    if mask.ndim != 1:
        raise TypeError("mask must be a 1D list-like")

    # infer dtype if needed
    if dtype is None:
        dtype = default_dtype
    else:
        dtype = dtype.numpy_dtype

    if is_integer_dtype(dtype) and values.dtype.kind == "f" and len(values) > 0:
        if mask.all():
            values = np.ones(values.shape, dtype=dtype)
        else:
            idx = np.nanargmax(values)
            if int(values[idx]) != original[idx]:
                # We have ints that lost precision during the cast.
                inferred_type = lib.infer_dtype(original, skipna=True)
                if (
                    inferred_type not in ["floating", "mixed-integer-float"]
                    and not mask.any()
                ):
                    values = np.asarray(original, dtype=dtype)
                else:
                    values = np.asarray(original, dtype="object")

    # we copy as need to coerce here
    if mask.any():
        values = values.copy()
        values[mask] = dtype_cls._internal_fill_value
    if inferred_type in ("string", "unicode"):
        # casts from str are always safe since they raise
        # a ValueError if the str cannot be parsed into a float
        values = values.astype(dtype, copy=copy)
    else:
        values = dtype_cls._safe_cast(values, dtype, copy=False)
    return values, mask

