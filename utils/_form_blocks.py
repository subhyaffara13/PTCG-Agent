import itertools

def _form_blocks(arrays: list[ArrayLike], consolidate: bool, refs: list) -> list[Block]:
    tuples = enumerate(arrays)

    if not consolidate:
        return _tuples_to_blocks_no_consolidate(tuples, refs)

    # when consolidating, we can ignore refs (either stacking always copies,
    # or the EA is already copied in the calling dict_to_mgr)

    # group by dtype
    grouper = itertools.groupby(tuples, _grouping_func)

    nbs: list[Block] = []
    for (_, dtype), tup_block in grouper:
        block_type = get_block_type(dtype)

        if isinstance(dtype, np.dtype):
            is_dtlike = dtype.kind in "mM"

            if issubclass(dtype.type, (str, bytes)):
                dtype = np.dtype(object)

            values, placement = _stack_arrays(tup_block, dtype)
            if is_dtlike:
                values = ensure_wrapped_if_datetimelike(values)
            blk = block_type(values, placement=BlockPlacement(placement), ndim=2)
            nbs.append(blk)

        elif is_1d_only_ea_dtype(dtype):
            dtype_blocks = [
                block_type(x[1], placement=BlockPlacement(x[0]), ndim=2)
                for x in tup_block
            ]
            nbs.extend(dtype_blocks)

        else:
            dtype_blocks = [
                block_type(
                    ensure_block_shape(x[1], 2), placement=BlockPlacement(x[0]), ndim=2
                )
                for x in tup_block
            ]
            nbs.extend(dtype_blocks)
    return nbs

