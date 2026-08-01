
def unpack_1tuple(tup):
    """
    If we have a length-1 tuple/list that contains a slice, unpack to just
    the slice.

    Notes
    -----
    The list case is deprecated.
    """
    if len(tup) == 1 and isinstance(tup[0], slice):
        # if we don't have a MultiIndex, we may still be able to handle
        #  a 1-tuple.  see test_1tuple_without_multiindex

        if isinstance(tup, list):
            # GH#31299
            raise ValueError(
                "Indexing with a single-item list containing a "
                "slice is not allowed. Pass a tuple instead.",
            )

        return tup[0]
    return tup

