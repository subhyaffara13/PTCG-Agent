
def _unpack_nested_dtype(other: Index) -> DtypeObj:
    """
    When checking if our dtype is comparable with another, we need
    to unpack CategoricalDtype to look at its categories.dtype.

    Parameters
    ----------
    other : Index

    Returns
    -------
    np.dtype or ExtensionDtype
    """
    dtype = other.dtype
    if isinstance(dtype, CategoricalDtype):
        # If there is ever a SparseIndex, this could get dispatched
        #  here too.
        return dtype.categories.dtype
    elif isinstance(dtype, ArrowDtype):
        # GH 53617
        import pyarrow as pa

        if pa.types.is_dictionary(dtype.pyarrow_dtype):
            other = other[:0].astype(ArrowDtype(dtype.pyarrow_dtype.value_type))
    return other.dtype

