
def _get_combined_index(
    indexes: list[Index],
    intersect: bool = False,
    sort: bool | lib.NoDefault = False,
) -> Index:
    """
    Return the union or intersection of indexes.

    Parameters
    ----------
    indexes : list of Index or list objects
        When intersect=True, do not accept list of lists.
    intersect : bool, default False
        If True, calculate the intersection between indexes. Otherwise,
        calculate the union.
    sort : bool, default False
        Whether the result index should come out sorted or not. NoDefault
        used for deprecation of GH#57335

    Returns
    -------
    Index
    """
    # TODO: handle index names!
    indexes = _get_distinct_objs(indexes)
    if len(indexes) == 0:
        index: Index = default_index(0)
    elif len(indexes) == 1:
        index = indexes[0]
    elif intersect:
        index = indexes[0]
        for other in indexes[1:]:
            index = index.intersection(other)
    else:
        index = union_indexes(indexes, sort=sort if sort is lib.no_default else False)
        index = ensure_index(index)

    if sort and sort is not lib.no_default:
        index = safe_sort_index(index)
    return index

