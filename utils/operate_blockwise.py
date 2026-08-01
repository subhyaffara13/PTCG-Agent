
def operate_blockwise(
    left: BlockManager, right: BlockManager, array_op
) -> BlockManager:
    # At this point we have already checked the parent DataFrames for
    #  assert rframe._indexed_same(lframe)

    res_blks: list[Block] = []
    for lvals, rvals, locs, left_ea, right_ea, rblk in _iter_block_pairs(left, right):
        res_values = array_op(lvals, rvals)
        if (
            left_ea
            and not right_ea
            and hasattr(res_values, "reshape")
            and not is_1d_only_ea_dtype(res_values.dtype)
        ):
            res_values = res_values.reshape(1, -1)
        nbs = rblk._split_op_result(res_values)

        # Assertions are disabled for performance, but should hold:
        # if right_ea or left_ea:
        #    assert len(nbs) == 1
        # else:
        #    assert res_values.shape == lvals.shape, (res_values.shape, lvals.shape)

        _reset_block_mgr_locs(nbs, locs)

        res_blks.extend(nbs)

    # Assertions are disabled for performance, but should hold:
    #  slocs = {y for nb in res_blks for y in nb.mgr_locs.as_array}
    #  nlocs = sum(len(nb.mgr_locs.as_array) for nb in res_blks)
    #  assert nlocs == len(left.items), (nlocs, len(left.items))
    #  assert len(slocs) == nlocs, (len(slocs), nlocs)
    #  assert slocs == set(range(nlocs)), slocs

    # TODO shallow copy axes?
    new_mgr = type(right)(tuple(res_blks), axes=right.axes, verify_integrity=False)
    return new_mgr

