
def ensure_index(index_like: Axes, copy: bool = False) -> Index:
    """
    Ensure that we have an index from some index-like object.

    Parameters
    ----------
    index_like : sequence
        An Index or other sequence
    copy : bool, default False

    Returns
    -------
    index : Index or MultiIndex

    See Also
    --------
    ensure_index_from_sequences

    Examples
    --------
    >>> ensure_index(["a", "b"])
    Index(['a', 'b'], dtype='str')

    >>> ensure_index([("a", "a"), ("b", "c")])
    Index([('a', 'a'), ('b', 'c')], dtype='object')

    >>> ensure_index([["a", "a"], ["b", "c"]])
    MultiIndex([('a', 'b'),
            ('a', 'c')],
           )
    """
    if isinstance(index_like, Index):
        if copy:
            index_like = index_like.copy()
        return index_like

    if isinstance(index_like, ABCSeries):
        name = index_like.name
        return Index(index_like, name=name, copy=copy)

    if is_iterator(index_like):
        index_like = list(index_like)

    if isinstance(index_like, list):
        if type(index_like) is not list:
            # must check for exactly list here because of strict type
            # check in clean_index_list
            index_like = list(index_like)

        if index_like and lib.is_all_arraylike(index_like):
            from pandas.core.indexes.multi import MultiIndex

            return MultiIndex.from_arrays(index_like)
        else:
            return Index(index_like, copy=copy, tupleize_cols=False)
    else:
        return Index(index_like, copy=copy)

