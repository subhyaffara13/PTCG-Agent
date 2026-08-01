
def maybe_droplevels(index: Index, key) -> Index:
    """
    Attempt to drop level or levels from the given index.

    Parameters
    ----------
    index: Index
    key : scalar or tuple

    Returns
    -------
    Index
    """
    # drop levels
    original_index = index
    if isinstance(key, tuple):
        # Caller is responsible for ensuring the key is not an entry in the first
        #  level of the MultiIndex.
        for _ in key:
            try:
                index = index._drop_level_numbers([0])
            except ValueError:
                # we have dropped too much, so back out
                return original_index
    else:
        try:
            index = index._drop_level_numbers([0])
        except ValueError:
            pass

    return index

