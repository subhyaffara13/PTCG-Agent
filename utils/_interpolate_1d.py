from typing import Any

def _interpolate_1d(
    indices: np.ndarray,
    yvalues: np.ndarray,
    method: str = "linear",
    limit: int | None = None,
    limit_direction: str = "forward",
    limit_area: Literal["inside", "outside"] | None = None,
    fill_value: Any | None = None,
    bounds_error: bool = False,
    order: int | None = None,
    mask=None,
    **kwargs,
) -> None:
    """
    Logic for the 1-d interpolation.  The input
    indices and yvalues will each be 1-d arrays of the same length.

    Bounds_error is currently hardcoded to False since non-scipy ones don't
    take it as an argument.

    Notes
    -----
    Fills 'yvalues' in-place.
    """
    if mask is not None:
        invalid = mask
    else:
        invalid = isna(yvalues)
    valid = ~invalid

    if not valid.any():
        return

    if valid.all():
        return

    # These index pointers to invalid values... i.e. {0, 1, etc...
    all_nans = np.flatnonzero(invalid)

    first_valid_index = find_valid_index(how="first", is_valid=valid)
    if first_valid_index is None:  # no nan found in start
        first_valid_index = 0
    start_nans = np.arange(first_valid_index)

    last_valid_index = find_valid_index(how="last", is_valid=valid)
    if last_valid_index is None:  # no nan found in end
        last_valid_index = len(yvalues)
    end_nans = np.arange(1 + last_valid_index, len(valid))

    # preserve_nans contains indices of invalid values,
    # but in this case, it is the final set of indices that need to be
    # preserved as NaN after the interpolation.

    # For example if limit_direction='forward' then preserve_nans will
    # contain indices of NaNs at the beginning of the series, and NaNs that
    # are more than 'limit' away from the prior non-NaN.

    # set preserve_nans based on direction using _interp_limit
    if limit_direction == "forward":
        preserve_nans = np.union1d(start_nans, _interp_limit(invalid, limit, 0))
    elif limit_direction == "backward":
        preserve_nans = np.union1d(end_nans, _interp_limit(invalid, 0, limit))
    else:
        # both directions... just use _interp_limit
        preserve_nans = np.unique(_interp_limit(invalid, limit, limit))

    # if limit_area is set, add either mid or outside indices
    # to preserve_nans GH #16284
    if limit_area == "inside":
        # preserve NaNs on the outside
        preserve_nans = np.union1d(preserve_nans, start_nans)
        preserve_nans = np.union1d(preserve_nans, end_nans)
    elif limit_area == "outside":
        # preserve NaNs on the inside
        mid_nans = np.setdiff1d(all_nans, start_nans, assume_unique=True)
        mid_nans = np.setdiff1d(mid_nans, end_nans, assume_unique=True)
        preserve_nans = np.union1d(preserve_nans, mid_nans)

    is_datetimelike = yvalues.dtype.kind in "mM"

    if is_datetimelike:
        yvalues = yvalues.view("i8")

    if method in NP_METHODS:
        # np.interp requires sorted X values, #21037

        indexer = np.argsort(indices[valid])
        yvalues[invalid] = np.interp(
            indices[invalid], indices[valid][indexer], yvalues[valid][indexer]
        )
    else:
        yvalues[invalid] = _interpolate_scipy_wrapper(
            indices[valid],
            yvalues[valid],
            indices[invalid],
            method=method,
            fill_value=fill_value,
            bounds_error=bounds_error,
            order=order,
            **kwargs,
        )

    if mask is not None:
        mask[:] = False
        mask[preserve_nans] = True
    elif is_datetimelike:
        yvalues[preserve_nans] = NaT.value
    else:
        yvalues[preserve_nans] = np.nan
    return

