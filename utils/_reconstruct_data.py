
def _reconstruct_data(
    values: ArrayLikeT, dtype: DtypeObj, original: AnyArrayLike
) -> ArrayLikeT:
    """
    reverse of _ensure_data

    Parameters
    ----------
    values : np.ndarray or ExtensionArray
    dtype : np.dtype or ExtensionDtype
    original : AnyArrayLike

    Returns
    -------
    ExtensionArray or np.ndarray
    """
    if isinstance(values, ABCExtensionArray) and values.dtype == dtype:
        # Catch DatetimeArray/TimedeltaArray
        return values

    if not isinstance(dtype, np.dtype):
        # i.e. ExtensionDtype; note we have ruled out above the possibility
        #  that values.dtype == dtype
        cls = dtype.construct_array_type()

        # error: Incompatible return value type
        # (got "ExtensionArray",
        # expected "ndarray[tuple[Any, ...], dtype[Any]]")
        return cls._from_sequence(values, dtype=dtype)  # type: ignore[return-value]

    # error: Incompatible return value type
    # (got "ndarray[tuple[Any, ...], dtype[Any]]",
    # expected "ExtensionArray")
    return values.astype(dtype, copy=False)  # type: ignore[return-value]

