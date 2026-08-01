
def get_block_type(dtype: DtypeObj) -> type[Block]:
    """
    Find the appropriate Block subclass to use for the given values and dtype.

    Parameters
    ----------
    dtype : numpy or pandas dtype

    Returns
    -------
    cls : class, subclass of Block
    """
    if isinstance(dtype, DatetimeTZDtype):
        return DatetimeLikeBlock
    elif isinstance(dtype, PeriodDtype):
        return NDArrayBackedExtensionBlock
    elif isinstance(dtype, ExtensionDtype):
        # Note: need to be sure NumpyExtensionArray is unwrapped before we get here
        return ExtensionBlock

    # We use kind checks because it is much more performant
    #  than is_foo_dtype
    kind = dtype.kind
    if kind in "Mm":
        return DatetimeLikeBlock

    return NumpyBlock

