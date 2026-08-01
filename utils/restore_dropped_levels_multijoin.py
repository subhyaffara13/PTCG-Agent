
def restore_dropped_levels_multijoin(
    left: MultiIndex,
    right: MultiIndex,
    dropped_level_names,
    join_index: Index,
    lindexer: npt.NDArray[np.intp],
    rindexer: npt.NDArray[np.intp],
) -> tuple[FrozenList, FrozenList, FrozenList]:
    """
    *this is an internal non-public method*

    Returns the levels, labels and names of a multi-index to multi-index join.
    Depending on the type of join, this method restores the appropriate
    dropped levels of the joined multi-index.
    The method relies on lindexer, rindexer which hold the index positions of
    left and right, where a join was feasible

    Parameters
    ----------
    left : MultiIndex
        left index
    right : MultiIndex
        right index
    dropped_level_names : str array
        list of non-common level names
    join_index : Index
        the index of the join between the
        common levels of left and right
    lindexer : np.ndarray[np.intp]
        left indexer
    rindexer : np.ndarray[np.intp]
        right indexer

    Returns
    -------
    levels : list of Index
        levels of combined multiindexes
    labels : np.ndarray[np.intp]
        labels of combined multiindexes
    names : List[Hashable]
        names of combined multiindex levels

    """

    def _convert_to_multiindex(index: Index) -> MultiIndex:
        if isinstance(index, MultiIndex):
            return index
        else:
            return MultiIndex.from_arrays([index._values], names=[index.name])

    # For multi-multi joins with one overlapping level,
    # the returned index if of type Index
    # Assure that join_index is of type MultiIndex
    # so that dropped levels can be appended
    join_index = _convert_to_multiindex(join_index)

    join_levels = join_index.levels
    join_codes = join_index.codes
    join_names = join_index.names

    # Iterate through the levels that must be restored
    for dropped_level_name in dropped_level_names:
        if dropped_level_name in left.names:
            idx = left
            indexer = lindexer
        else:
            idx = right
            indexer = rindexer

        # The index of the level name to be restored
        name_idx = idx.names.index(dropped_level_name)

        restore_levels = idx.levels[name_idx]
        # Inject -1 in the codes list where a join was not possible
        # IOW indexer[i]=-1
        codes = idx.codes[name_idx]
        if indexer is None:
            restore_codes = codes
        else:
            restore_codes = algos.take_nd(codes, indexer, fill_value=-1)

        # Use + operator: FrozenList.__add__ returns FrozenList, unpacking returns list
        join_levels = join_levels + [restore_levels]  # noqa: RUF005
        join_codes = join_codes + [restore_codes]  # noqa: RUF005
        join_names = join_names + [dropped_level_name]  # noqa: RUF005

    return join_levels, join_codes, join_names

