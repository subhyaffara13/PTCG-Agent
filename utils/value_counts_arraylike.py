
def value_counts_arraylike(
    values: np.ndarray, dropna: bool, mask: npt.NDArray[np.bool_] | None = None
) -> tuple[ArrayLike, npt.NDArray[np.int64], int]:
    """
    Parameters
    ----------
    values : np.ndarray
    dropna : bool
    mask : np.ndarray[bool] or None, default None

    Returns
    -------
    uniques : np.ndarray
    counts : np.ndarray[np.int64]
    """
    original = values
    values = _ensure_data(values)

    keys, counts, na_counter = htable.value_count(values, dropna, mask=mask)

    if needs_i8_conversion(original.dtype):
        # datetime, timedelta, or period

        if dropna:
            mask = keys != iNaT
            keys, counts = keys[mask], counts[mask]

    res_keys = _reconstruct_data(keys, original.dtype, original)
    return res_keys, counts, na_counter

