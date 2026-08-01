
def maybe_cast_to_integer_array(arr: list | np.ndarray, dtype: np.dtype) -> np.ndarray:
    """
    Takes any dtype and returns the casted version, raising for when data is
    incompatible with integer/unsigned integer dtypes.

    Parameters
    ----------
    arr : np.ndarray or list
        The array to cast.
    dtype : np.dtype
        The integer dtype to cast the array to.

    Returns
    -------
    ndarray
        Array of integer or unsigned integer dtype.

    Raises
    ------
    OverflowError : the dtype is incompatible with the data
    ValueError : loss of precision has occurred during casting

    Examples
    --------
    If you try to coerce negative values to unsigned integers, it raises:

    >>> pd.Series([-1], dtype="uint64")
    Traceback (most recent call last):
        ...
    OverflowError: Trying to coerce negative values to unsigned integers

    Also, if you try to coerce float values to integers, it raises:

    >>> maybe_cast_to_integer_array([1, 2, 3.5], dtype=np.dtype("int64"))
    Traceback (most recent call last):
        ...
    ValueError: Trying to coerce float values to integers
    """
    assert dtype.kind in "iu"

    try:
        if not isinstance(arr, np.ndarray):
            with warnings.catch_warnings():
                # We already disallow dtype=uint w/ negative numbers
                # (test_constructor_coercion_signed_to_unsigned) so safe to ignore.
                warnings.filterwarnings(
                    "ignore",
                    "NumPy will stop allowing conversion of out-of-bound Python int",
                    DeprecationWarning,
                )
                casted = np.asarray(arr, dtype=dtype)
        else:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning)
                casted = arr.astype(dtype, copy=False)
    except OverflowError as err:
        raise OverflowError(
            "The elements provided in the data cannot all be "
            f"casted to the dtype {dtype}"
        ) from err

    if isinstance(arr, np.ndarray) and arr.dtype == dtype:
        # avoid expensive array_equal check
        return casted

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings(
            "ignore", "elementwise comparison failed", FutureWarning
        )
        if np.array_equal(arr, casted):
            return casted

    # We do this casting to allow for proper
    # data and dtype checking.
    #
    # We didn't do this earlier because NumPy
    # doesn't handle `uint64` correctly.
    arr = np.asarray(arr)

    if np.issubdtype(arr.dtype, str):
        # TODO(numpy-2.0 min): This case will raise an OverflowError above
        if (casted.astype(str) == arr).all():
            return casted
        raise ValueError(f"string values cannot be losslessly cast to {dtype}")

    if dtype.kind == "u" and (arr < 0).any():
        # TODO: can this be hit anymore after numpy 2.0?
        raise OverflowError("Trying to coerce negative values to unsigned integers")

    if arr.dtype.kind == "f":
        if not np.isfinite(arr).all():
            raise IntCastingNaNError(
                "Cannot convert non-finite values (NA or inf) to integer"
            )
        raise ValueError("Trying to coerce float values to integers")
    if arr.dtype == object:
        raise ValueError("Trying to coerce object values to integers")

    if casted.dtype < arr.dtype:
        # TODO: Can this path be hit anymore with numpy > 2
        # GH#41734 e.g. [1, 200, 923442] and dtype="int8" -> overflows
        raise ValueError(
            f"Values are too large to be losslessly converted to {dtype}. "
            f"To cast anyway, use pd.Series(values).astype({dtype})"
        )

    if arr.dtype.kind in "mM":
        # test_constructor_maskedarray_nonfloat
        raise TypeError(
            f"Constructing a Series or DataFrame from {arr.dtype} values and "
            f"dtype={dtype} is not supported. Use values.view({dtype}) instead."
        )

    # No known cases that get here, but raising explicitly to cover our bases.
    raise ValueError(f"values cannot be losslessly cast to {dtype}")

