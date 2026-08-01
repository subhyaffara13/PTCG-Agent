
def rank(A, eps):
    S = np.linalg.svd(A, compute_uv=False)
    try:
        rank = np.nonzero(S < eps)[0][0]
    except IndexError:
        rank = A.shape[0]
    return rank


def rank(
    values: ArrayLike,
    axis: AxisInt = 0,
    method: str = "average",
    na_option: str = "keep",
    ascending: bool = True,
    pct: bool = False,
    mask: npt.NDArray[np.bool_] | None = None,
) -> npt.NDArray[np.float64]:
    """
    Rank the values along a given axis.

    Parameters
    ----------
    values : np.ndarray or ExtensionArray
        Array whose values will be ranked. The number of dimensions in this
        array must not exceed 2.
    axis : int, default 0
        Axis over which to perform rankings.
    method : {'average', 'min', 'max', 'first', 'dense'}, default 'average'
        The method by which tiebreaks are broken during the ranking.
    na_option : {'keep', 'top'}, default 'keep'
        The method by which NaNs are placed in the ranking.
        - ``keep``: rank each NaN value with a NaN ranking
        - ``top``: replace each NaN with either +/- inf so that they
                   there are ranked at the top
    ascending : bool, default True
        Whether or not the elements should be ranked in ascending order.
    pct : bool, default False
        Whether or not to the display the returned rankings in integer form
        (e.g. 1, 2, 3) or in percentile form (e.g. 0.333..., 0.666..., 1).
    mask : bool ndarray, optional
        Boolean array indicating which elements to exclude from ranking.
    """
    is_datetimelike = needs_i8_conversion(values.dtype)
    values = _ensure_data(values)

    if values.ndim == 1:
        ranks = algos.rank_1d(
            values,
            is_datetimelike=is_datetimelike,
            ties_method=method,
            ascending=ascending,
            na_option=na_option,
            pct=pct,
            mask=mask,
        )
    elif values.ndim == 2:
        assert mask is None
        ranks = algos.rank_2d(
            values,
            axis=axis,
            is_datetimelike=is_datetimelike,
            ties_method=method,
            ascending=ascending,
            na_option=na_option,
            pct=pct,
        )
    else:
        raise TypeError("Array with ndim > 2 are not supported.")

    return ranks


def rank(memref: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return RankOp(memref=memref, results=results, loc=loc, ip=ip).result

