
def cast_scalar_indexer(val):
    """
    Disallow indexing with a float key, even if that key is a round number.

    Parameters
    ----------
    val : scalar

    Returns
    -------
    outval : scalar
    """
    # assumes lib.is_scalar(val)
    if lib.is_float(val) and val.is_integer():
        raise IndexError(
            # GH#34193
            "Indexing with a float is no longer supported. Manually convert "
            "to an integer key instead."
        )
    return val

