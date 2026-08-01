
def _nanquantile_1d(
    values: np.ndarray,
    mask: npt.NDArray[np.bool_],
    qs: npt.NDArray[np.float64],
    na_value: Scalar,
    interpolation: str,
) -> Scalar | np.ndarray:
    """
    Wrapper for np.quantile that skips missing values, specialized to
    1-dimensional case.

    Parameters
    ----------
    values : array over which to find quantiles
    mask : ndarray[bool]
        locations in values that should be considered missing
    qs : np.ndarray[float64] of quantile indices to find
    na_value : scalar
        value to return for empty or all-null values
    interpolation : str

    Returns
    -------
    quantiles : scalar or array
    """
    # mask is Union[ExtensionArray, ndarray]
    values = values[~mask]

    if len(values) == 0:
        # Can't pass dtype=values.dtype here bc we might have na_value=np.nan
        #  with values.dtype=int64 see test_quantile_empty
        # equiv: 'np.array([na_value] * len(qs))' but much faster
        return np.full(len(qs), na_value)

    return np.quantile(
        values,
        qs,
        # error: No overload variant of "percentile" matches argument
        # types "ndarray[Any, Any]", "ndarray[Any, dtype[floating[_64Bit]]]"
        # , "Dict[str, str]"  [call-overload]
        method=interpolation,  # type: ignore[call-overload]
    )


def _nanquantile_1d(
    arr1d, q, overwrite_input=False, method="linear", weights=None,
    weak_q=False,
):
    """
    Private function for rank 1 arrays. Compute quantile ignoring NaNs.
    See nanpercentile for parameter usage
    """
    # TODO: What to do when arr1d = [1, np.nan] and weights = [0, 1]?
    arr1d, weights, overwrite_input = _remove_nan_1d(arr1d,
        second_arr1d=weights, overwrite_input=overwrite_input)
    if arr1d.size == 0:
        # convert to scalar
        return np.full(q.shape, np.nan, dtype=arr1d.dtype)[()]

    return fnb._quantile_unchecked(
        arr1d,
        q,
        overwrite_input=overwrite_input,
        method=method,
        weights=weights,
        weak_q=weak_q,
    )

