
def exclusive_scan_decoupled_lookback(
    scratch_base,
    block_value,
    index,
    combine_fn,
    DTYPE_VALUE_AS_UINT: tl.constexpr,
    DTYPE_PACK: tl.constexpr,
):
    """Compute exclusive scan of a scalar value between blocks

    Ref: https://research.nvidia.com/publication/2016-03_single-pass-parallel-prefix-scan-decoupled-look-back

    scratch_base: Pointer to scratch space in global memory
    block_value: Scalar value for this block
    index: Scalar index of this block relative to the current scan
    combine_fn: Function ``(value, value) -> value`` which is scanned over
    DTYPE_VALUE_AS_UINT: A tl.uint{n} type equal in size to ``block_value``
    DTYPE_PACK: Unsigned type twice the width of block_value

    NOTE: This function is limited to values which are 32-bits or less because
    we need to pack (value, flag) into a single unsigned int.
    """
    # Publish block sum so subsequent blocks don't get stuck waiting for us
    DTYPE_VALUE = block_value.dtype
    pack = pack_value_flag(
        block_value,
        tl.full(block_value.shape, 1, DTYPE_VALUE_AS_UINT),
        DTYPE_VALUE_AS_UINT,
        DTYPE_PACK,
    )
    if index > 0:
        tl.atomic_xchg(scratch_base + index, pack, sem="relaxed")

    # Calculate exclusive prefix scan
    exclusive_prefix = tl.zeros([], DTYPE_VALUE)
    prefix_valid = False
    test_target = index - 1
    while test_target >= 0:
        # tl.atomic_load
        flag = tl.full([], 0, DTYPE_VALUE_AS_UINT)
        while flag == 0:
            pack = tl.atomic_add(scratch_base + test_target, 0, sem="relaxed")
            flag = unpack_flag(pack, DTYPE_VALUE_AS_UINT)

        value = unpack_value(pack, DTYPE_VALUE, DTYPE_VALUE_AS_UINT)
        if prefix_valid:
            exclusive_prefix = combine_fn(value, exclusive_prefix)
        else:
            exclusive_prefix = value
            prefix_valid = True

        if flag == 2:
            test_target = -1
        else:
            test_target = test_target - 1

    # Make inclusive block sum visible to other blocks
    if prefix_valid:
        inclusive_prefix = combine_fn(exclusive_prefix, block_value)
    else:
        inclusive_prefix = block_value
    pack = pack_value_flag(
        inclusive_prefix,
        tl.full([], 2, DTYPE_VALUE_AS_UINT),
        DTYPE_VALUE_AS_UINT,
        DTYPE_PACK,
    )
    tl.atomic_xchg(scratch_base + index, pack, sem="relaxed")
    return exclusive_prefix

