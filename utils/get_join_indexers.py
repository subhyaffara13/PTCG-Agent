
def get_join_indexers(
    left_keys: list[ArrayLike],
    right_keys: list[ArrayLike],
    sort: bool = False,
    how: JoinHow = "inner",
) -> tuple[npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:
    """

    Parameters
    ----------
    left_keys : list[ndarray, ExtensionArray, Index, Series]
    right_keys : list[ndarray, ExtensionArray, Index, Series]
    sort : bool, default False
    how : {'inner', 'outer', 'left', 'right'}, default 'inner'

    Returns
    -------
    np.ndarray[np.intp] or None
        Indexer into the left_keys.
    np.ndarray[np.intp] or None
        Indexer into the right_keys.
    """
    assert len(left_keys) == len(right_keys), (
        "left_keys and right_keys must be the same length"
    )

    # fast-path for empty left/right
    left_n = len(left_keys[0])
    right_n = len(right_keys[0])
    if left_n == 0:
        if how in ["left", "inner"]:
            return _get_empty_indexer()
        elif not sort and how in ["right", "outer"]:
            return _get_no_sort_one_missing_indexer(right_n, True)
    elif right_n == 0:
        if how in ["right", "inner"]:
            return _get_empty_indexer()
        elif not sort and how in ["left", "outer"]:
            return _get_no_sort_one_missing_indexer(left_n, False)

    lkey: ArrayLike
    rkey: ArrayLike
    if len(left_keys) > 1:
        # get left & right join labels and num. of levels at each location
        mapped = (
            _factorize_keys(left_keys[n], right_keys[n], sort=sort)
            for n in range(len(left_keys))
        )
        zipped = zip(*mapped, strict=True)
        llab, rlab, shape = (list(x) for x in zipped)

        # get flat i8 keys from label lists
        lkey, rkey = _get_join_keys(llab, rlab, tuple(shape), sort)
    else:
        lkey = left_keys[0]
        rkey = right_keys[0]

    left = Index(lkey, copy=False)
    right = Index(rkey, copy=False)

    if (
        left.is_monotonic_increasing
        and right.is_monotonic_increasing
        and (left.is_unique or right.is_unique)
    ):
        _, lidx, ridx = left.join(right, how=how, return_indexers=True, sort=sort)
    else:
        lidx, ridx = get_join_indexers_non_unique(
            left._values, right._values, sort, how
        )

    if lidx is not None and is_range_indexer(lidx, len(left)):
        lidx = None
    if ridx is not None and is_range_indexer(ridx, len(right)):
        ridx = None
    return lidx, ridx

