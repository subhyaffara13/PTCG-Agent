
def unique_with_mask(values, mask: npt.NDArray[np.bool_] | None = None):
    """See algorithms.unique for docs. Takes a mask for masked arrays."""
    values = _ensure_arraylike(values, func_name="unique")

    if isinstance(values.dtype, ExtensionDtype):
        # Dispatch to extension dtype's unique.
        return values.unique()

    if isinstance(values, ABCIndex):
        # Dispatch to Index's unique.
        return values.unique()

    original = values
    hashtable, values = _get_hashtable_algo(values)

    table = hashtable(len(values))
    if mask is None:
        uniques = table.unique(values)
        uniques = _reconstruct_data(uniques, original.dtype, original)
        return uniques

    else:
        uniques, mask = table.unique(values, mask=mask)
        uniques = _reconstruct_data(uniques, original.dtype, original)
        assert mask is not None  # for mypy
        return uniques, mask.astype("bool")

