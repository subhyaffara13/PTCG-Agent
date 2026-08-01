
def get_join_indexers_non_unique(
    left: ArrayLike,
    right: ArrayLike,
    sort: bool = False,
    how: JoinHow = "inner",
) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
    """
    Get join indexers for left and right.

    Parameters
    ----------
    left : ArrayLike
    right : ArrayLike
    sort : bool, default False
    how : {'inner', 'outer', 'left', 'right'}, default 'inner'

    Returns
    -------
    np.ndarray[np.intp]
        Indexer into left.
    np.ndarray[np.intp]
        Indexer into right.
    """
    lkey, rkey, count = _factorize_keys(left, right, sort=sort, how=how)
    if count == -1:
        # hash join
        return lkey, rkey
    if how == "left":
        lidx, ridx = libjoin.left_outer_join(lkey, rkey, count, sort=sort)
    elif how == "right":
        ridx, lidx = libjoin.left_outer_join(rkey, lkey, count, sort=sort)
    elif how == "inner":
        lidx, ridx = libjoin.inner_join(lkey, rkey, count, sort=sort)
    elif how == "outer":
        lidx, ridx = libjoin.full_outer_join(lkey, rkey, count)
    return lidx, ridx

