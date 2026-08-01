
def check_bool_indexer(index: Index, key) -> np.ndarray:
    """
    Check if key is a valid boolean indexer for an object with such index and
    perform reindexing or conversion if needed.

    This function assumes that is_bool_indexer(key) == True.

    Parameters
    ----------
    index : Index
        Index of the object on which the indexing is done.
    key : list-like
        Boolean indexer to check.

    Returns
    -------
    np.array
        Resulting key.

    Raises
    ------
    IndexError
        If the key does not have the same length as index.
    IndexingError
        If the index of the key is unalignable to index.
    """
    result = key
    if isinstance(key, ABCSeries) and not key.index.equals(index):
        indexer = result.index.get_indexer_for(index)
        if -1 in indexer:
            raise IndexingError(
                "Unalignable boolean Series provided as "
                "indexer (index of the boolean Series and of "
                "the indexed object do not match)."
            )

        result = result.take(indexer)

        # fall through for boolean
        if not isinstance(result.dtype, ExtensionDtype):
            return result.astype(bool)._values

    if is_object_dtype(key):
        # key might be object-dtype bool, check_array_indexer needs bool array
        result = np.asarray(result, dtype=bool)
    elif not is_array_like(result):
        # GH 33924
        # key may contain nan elements, check_array_indexer needs bool array
        result = pd_array(result, dtype=bool)
    return check_array_indexer(index, result)

