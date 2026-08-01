
def get_indexer_indexer(
    target: Index,
    level: Level | list[Level] | None,
    ascending: list[bool] | bool,
    kind: SortKind,
    na_position: NaPosition,
    sort_remaining: bool,
    key: IndexKeyFunc,
) -> npt.NDArray[np.intp] | None:
    """
    Helper method that return the indexer according to input parameters for
    the sort_index method of DataFrame and Series.

    Parameters
    ----------
    target : Index
    level : int or level name or list of ints or list of level names
    ascending : bool or list of bools, default True
    kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}
    na_position : {'first', 'last'}
    sort_remaining : bool
    key : callable, optional

    Returns
    -------
    Optional[ndarray[intp]]
        The indexer for the new index.
    """

    # error: Incompatible types in assignment (expression has type
    # "Union[ExtensionArray, ndarray[Any, Any], Index, Series]", variable has
    # type "Index")
    target = ensure_key_mapped(target, key, levels=level)  # type: ignore[assignment]
    target = target._sort_levels_monotonic()

    if level is not None:
        _, indexer = target.sortlevel(
            level,
            ascending=ascending,
            sort_remaining=sort_remaining,
            na_position=na_position,
        )
    elif (np.all(ascending) and target.is_monotonic_increasing) or (
        not np.any(ascending) and target.is_monotonic_decreasing
    ):
        # Check monotonic-ness before sort an index (GH 11080)
        return None
    elif isinstance(target, ABCMultiIndex):
        codes = [lev.codes for lev in target._get_codes_for_sorting()]
        indexer = lexsort_indexer(
            codes, orders=ascending, na_position=na_position, codes_given=True
        )
    else:
        # ascending can only be a Sequence for MultiIndex
        indexer = nargsort(
            target,
            kind=kind,
            ascending=cast(bool, ascending),
            na_position=na_position,
        )
    return indexer

