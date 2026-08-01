
def factorize_array(
    values: np.ndarray,
    use_na_sentinel: bool = True,
    size_hint: int | None = None,
    na_value: object = None,
    mask: npt.NDArray[np.bool_] | None = None,
) -> tuple[npt.NDArray[np.intp], np.ndarray]:
    """
    Factorize a numpy array to codes and uniques.

    This doesn't do any coercion of types or unboxing before factorization.

    Parameters
    ----------
    values : ndarray
    use_na_sentinel : bool, default True
        If True, the sentinel -1 will be used for NaN values. If False,
        NaN values will be encoded as non-negative integers and will not drop the
        NaN from the uniques of the values.
    size_hint : int, optional
        Passed through to the hashtable's 'get_labels' method
    na_value : object, optional
        A value in `values` to consider missing. Note: only use this
        parameter when you know that you don't have any values pandas would
        consider missing in the array (NaN for float data, iNaT for
        datetimes, etc.).
    mask : ndarray[bool], optional
        If not None, the mask is used as indicator for missing values
        (True = missing, False = valid) instead of `na_value` or
        condition "val != val".

    Returns
    -------
    codes : ndarray[np.intp]
    uniques : ndarray
    """
    original = values
    if values.dtype.kind in "mM":
        # _get_hashtable_algo will cast dt64/td64 to i8 via _ensure_data, so we
        #  need to do the same to na_value. We are assuming here that the passed
        #  na_value is an appropriately-typed NaT.
        # e.g. test_where_datetimelike_categorical
        na_value = iNaT

    hash_klass, values = _get_hashtable_algo(values)

    table = hash_klass(size_hint or len(values))
    uniques, codes = table.factorize(
        values,
        na_sentinel=-1,
        na_value=na_value,
        mask=mask,
        ignore_na=use_na_sentinel,
    )

    # re-cast e.g. i8->dt64/td64, uint8->bool
    uniques = _reconstruct_data(uniques, original.dtype, original)

    codes = ensure_platform_int(codes)
    return codes, uniques

