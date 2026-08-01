
def sanitize_array(
    data,
    index: Index | None,
    dtype: DtypeObj | None = None,
    copy: bool = False,
    *,
    allow_2d: bool = False,
) -> ArrayLike:
    """
    Sanitize input data to an ndarray or ExtensionArray, copy if specified,
    coerce to the dtype if specified.

    Parameters
    ----------
    data : Any
    index : Index or None, default None
    dtype : np.dtype, ExtensionDtype, or None, default None
    copy : bool, default False
    allow_2d : bool, default False
        If False, raise if we have a 2D Arraylike.

    Returns
    -------
    np.ndarray or ExtensionArray
    """
    original_dtype = dtype
    if isinstance(data, ma.MaskedArray):
        data = sanitize_masked_array(data)

    if isinstance(dtype, NumpyEADtype):
        # Avoid ending up with a NumpyExtensionArray
        dtype = dtype.numpy_dtype

    infer_object = not isinstance(data, (ABCIndex, ABCSeries))

    # extract ndarray or ExtensionArray, ensure we have no NumpyExtensionArray
    data = extract_array(data, extract_numpy=True, extract_range=True)

    if isinstance(data, np.ndarray) and data.ndim == 0:
        if dtype is None:
            dtype = data.dtype
        data = lib.item_from_zerodim(data)
    elif isinstance(data, range):
        # GH#16804
        data = range_to_ndarray(data)
        copy = False

    if not is_list_like(data):
        if index is None:
            raise ValueError("index must be specified when data is not list-like")
        if isinstance(data, str) and using_string_dtype() and original_dtype is None:
            from pandas.core.arrays.string_ import StringDtype

            dtype = StringDtype(na_value=np.nan)
        data = construct_1d_arraylike_from_scalar(data, len(index), dtype)

        return data

    elif isinstance(data, ABCExtensionArray):
        # it is already ensured above this is not a NumpyExtensionArray
        # Until GH#49309 is fixed this check needs to come before the
        #  ExtensionDtype check
        if dtype is not None:
            subarr = data.astype(dtype, copy=copy)
        elif copy:
            subarr = data.copy()
        else:
            subarr = data

    elif isinstance(dtype, ExtensionDtype):
        # create an extension array from its dtype
        _sanitize_non_ordered(data)
        cls = dtype.construct_array_type()
        if not hasattr(data, "__array__"):
            data = list(data)
        subarr = cls._from_sequence(data, dtype=dtype, copy=copy)

    # GH#846
    elif isinstance(data, np.ndarray):
        if isinstance(data, np.matrix):
            data = data.A

        if dtype is None:
            subarr = data
            if data.dtype == object and infer_object:
                subarr = lib.maybe_convert_objects(
                    data,
                    # Here we do not convert numeric dtypes, as if we wanted that,
                    #  numpy would have done it for us.
                    convert_numeric=False,
                    convert_non_numeric=True,
                    convert_to_nullable_dtype=False,
                    dtype_if_all_nat=np.dtype("M8[s]"),
                )
            elif data.dtype.kind == "U" and using_string_dtype():
                from pandas.core.arrays.string_ import StringDtype

                dtype = StringDtype(na_value=np.nan)
                subarr = dtype.construct_array_type()._from_sequence(data, dtype=dtype)

            if (
                subarr is data
                or (subarr.dtype == "str" and subarr.dtype.storage == "python")  # type: ignore[union-attr]
            ) and copy:
                subarr = subarr.copy()

        else:
            # we will try to copy by-definition here
            subarr = _try_cast(data, dtype, copy)

    elif hasattr(data, "__array__"):
        # e.g. dask array GH#38645
        if not copy:
            data = np.asarray(data)
        else:
            data = np.array(data, copy=copy)
        return sanitize_array(
            data,
            index=index,
            dtype=dtype,
            copy=False,
            allow_2d=allow_2d,
        )

    else:
        _sanitize_non_ordered(data)
        # materialize e.g. generators, convert e.g. tuples, abc.ValueView
        data = list(data)

        if len(data) == 0 and dtype is None:
            # We default to float64, matching numpy
            subarr = np.array([], dtype=np.float64)

        elif dtype is not None:
            subarr = _try_cast(data, dtype, copy)

        else:
            subarr = maybe_convert_platform(data)
            if subarr.dtype == object:
                subarr = cast(np.ndarray, subarr)
                subarr = lib.maybe_convert_objects(
                    subarr,
                    # Here we do not convert numeric dtypes, as if we wanted that,
                    #  numpy would have done it for us.
                    convert_numeric=False,
                    convert_non_numeric=True,
                    convert_to_nullable_dtype=False,
                    dtype_if_all_nat=np.dtype("M8[s]"),
                )

    subarr = _sanitize_ndim(subarr, data, dtype, index, allow_2d=allow_2d)

    if isinstance(subarr, np.ndarray):
        # at this point we should have dtype be None or subarr.dtype == dtype
        dtype = cast(np.dtype, dtype)
        subarr = _sanitize_str_dtypes(subarr, data, dtype, copy)

    return subarr

