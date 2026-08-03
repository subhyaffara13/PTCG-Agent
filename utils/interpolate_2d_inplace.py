from typing import Any

def interpolate_2d_inplace(
    data: np.ndarray,  # floating dtype
    index: Index,
    axis: AxisInt,
    method: str = "linear",
    limit: int | None = None,
    limit_direction: str = "forward",
    limit_area: str | None = None,
    fill_value: Any | None = None,
    mask=None,
    **kwargs,
) -> None:
    """
    Column-wise application of _interpolate_1d.

    Notes
    -----
    Alters 'data' in-place.

    The signature does differ from _interpolate_1d because it only
    includes what is needed for Block.interpolate.
    """
    # validate the interp method
    clean_interp_method(method, index, **kwargs)

    if is_valid_na_for_dtype(fill_value, data.dtype):
        fill_value = na_value_for_dtype(data.dtype, compat=False)

    if method == "time":
        if not needs_i8_conversion(index.dtype):
            raise ValueError(
                "time-weighted interpolation only works "
                "on Series or DataFrames with a "
                "DatetimeIndex"
            )
        method = "values"

    limit_direction = validate_limit_direction(limit_direction)
    limit_area_validated = validate_limit_area(limit_area)

    # default limit is unlimited GH #16282
    limit = algos.validate_limit(nobs=None, limit=limit)

    indices = _index_to_interp_indices(index, method)

    def func(yvalues: np.ndarray) -> None:
        # process 1-d slices in the axis direction

        _interpolate_1d(
            indices=indices,
            yvalues=yvalues,
            method=method,
            limit=limit,
            limit_direction=limit_direction,
            limit_area=limit_area_validated,
            fill_value=fill_value,
            bounds_error=False,
            mask=mask,
            **kwargs,
        )

    np.apply_along_axis(func, axis, data)

