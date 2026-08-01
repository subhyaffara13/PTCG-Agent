
def _get_empty_dtype(join_units: Sequence[JoinUnit]) -> DtypeObj:
    """
    Return dtype and N/A values to use when concatenating specified units.

    Returned N/A value may be None which means there was no casting involved.

    Returns
    -------
    dtype
    """
    if lib.dtypes_all_equal([ju.block.dtype for ju in join_units]):
        empty_dtype = join_units[0].block.dtype
        return empty_dtype

    has_none_blocks = any(unit.block.dtype.kind == "V" for unit in join_units)

    dtypes = [unit.block.dtype for unit in join_units if not unit.is_na]

    dtype = find_common_type(dtypes)
    if has_none_blocks:
        dtype = ensure_dtype_can_hold_na(dtype)

    return dtype

