
def nanall(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    mask: npt.NDArray[np.bool_] | None = None,
) -> bool:
    """
    Check if all elements along an axis evaluate to True.

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : bool

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, 2, np.nan])
    >>> nanops.nanall(s.values)
    np.True_

    >>> from pandas.core import nanops
    >>> s = pd.Series([1, 0])
    >>> nanops.nanall(s.values)
    np.False_
    """
    if values.dtype.kind in "iub" and mask is None:
        # GH#26032 fastpath
        # error: Incompatible return value type (got "Union[bool_, ndarray]",
        # expected "bool")
        return values.all(axis)  # type: ignore[return-value]

    if values.dtype.kind == "M":
        # GH#34479
        raise TypeError("datetime64 type does not support operation 'all'")

    values, _ = _get_values(values, skipna, fill_value=True, mask=mask)

    # For object type, all won't necessarily return
    # boolean values (numpy/numpy#4352)
    if values.dtype == object:
        values = values.astype(bool)

    # error: Incompatible return value type (got "Union[bool_, ndarray]", expected
    # "bool")
    return values.all(axis)  # type: ignore[return-value]

