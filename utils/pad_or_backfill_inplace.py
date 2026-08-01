
def pad_or_backfill_inplace(
    values: np.ndarray,
    method: Literal["pad", "backfill"] = "pad",
    axis: AxisInt = 0,
    limit: int | None = None,
    limit_area: Literal["inside", "outside"] | None = None,
) -> None:
    """
    Perform an actual interpolation of values, values will be make 2-d if
    needed fills inplace, returns the result.

    Parameters
    ----------
    values: np.ndarray
        Input array.
    method: str, default "pad"
        Interpolation method. Could be "bfill" or "pad"
    axis: 0 or 1
        Interpolation axis
    limit: int, optional
        Index limit on interpolation.
    limit_area: str, optional
        Limit area for interpolation. Can be "inside" or "outside"

    Notes
    -----
    Modifies values in-place.
    """
    transf = (lambda x: x) if axis == 0 else (lambda x: x.T)

    # reshape a 1 dim if needed
    if values.ndim == 1:
        if axis != 0:  # pragma: no cover
            raise AssertionError("cannot interpolate on an ndim == 1 with axis != 0")
        values = values.reshape((1, *values.shape))

    method = clean_fill_method(method)
    tvalues = transf(values)

    func = get_fill_func(method, ndim=2)
    # _pad_2d and _backfill_2d both modify tvalues inplace
    func(tvalues, limit=limit, limit_area=limit_area)

