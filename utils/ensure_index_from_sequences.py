
def ensure_index_from_sequences(sequences, names=None) -> Index:
    """
    Construct an index from sequences of data.

    A single sequence returns an Index. Many sequences returns a
    MultiIndex.

    Parameters
    ----------
    sequences : sequence of sequences
    names : sequence of str

    Returns
    -------
    index : Index or MultiIndex

    Examples
    --------
    >>> ensure_index_from_sequences([[1, 2, 4]], names=["name"])
    Index([1, 2, 4], dtype='int64', name='name')

    >>> ensure_index_from_sequences([["a", "a"], ["a", "b"]], names=["L1", "L2"])
    MultiIndex([('a', 'a'),
                ('a', 'b')],
               names=['L1', 'L2'])

    See Also
    --------
    ensure_index
    """
    from pandas.core.indexes.api import default_index
    from pandas.core.indexes.multi import MultiIndex

    if len(sequences) == 0:
        return default_index(0)
    elif len(sequences) == 1:
        if names is not None:
            names = names[0]
        return Index(maybe_sequence_to_range(sequences[0]), name=names)
    else:
        # TODO: Apply maybe_sequence_to_range to sequences?
        return MultiIndex.from_arrays(sequences, names=names)

