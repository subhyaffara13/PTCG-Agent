
def _try_cast(
    arr: list | np.ndarray,
    dtype: np.dtype,
    copy: bool,
) -> ArrayLike:
    """
    Convert input to numpy ndarray and optionally cast to a given dtype.

    Parameters
    ----------
    arr : ndarray or list
        Excludes: ExtensionArray, Series, Index.
    dtype : np.dtype
    copy : bool
        If False, don't copy the data if not needed.

    Returns
    -------
    np.ndarray or ExtensionArray
    """
    is_ndarray = isinstance(arr, np.ndarray)

    if dtype == object:
        if not is_ndarray:
            subarr = construct_1d_object_array_from_listlike(arr)
            return subarr
        return ensure_wrapped_if_datetimelike(arr).astype(dtype, copy=copy)

    elif dtype.kind == "U":
        # TODO: test cases with arr.dtype.kind in "mM"
        if is_ndarray:
            arr = cast(np.ndarray, arr)
            shape = arr.shape
            if arr.ndim > 1:
                arr = arr.ravel()
        else:
            shape = (len(arr),)
        return lib.ensure_string_array(arr, convert_na_value=False, copy=copy).reshape(
            shape
        )

    elif dtype.kind in "mM":
        if is_ndarray:
            arr = cast(np.ndarray, arr)
            if arr.ndim == 2 and arr.shape[1] == 1:
                # GH#60081: DataFrame Constructor converts 1D data to array of
                # shape (N, 1), but maybe_cast_to_datetime assumes 1D input
                return maybe_cast_to_datetime(arr[:, 0], dtype).reshape(arr.shape)
        return maybe_cast_to_datetime(arr, dtype)

    # GH#15832: Check if we are requesting a numeric dtype and
    # that we can convert the data to the requested dtype.
    elif dtype.kind in "iu":
        # this will raise if we have e.g. floats

        subarr = maybe_cast_to_integer_array(arr, dtype)
    elif not copy:
        subarr = np.asarray(arr, dtype=dtype)
    else:
        subarr = np.array(arr, dtype=dtype, copy=copy)

    return subarr

