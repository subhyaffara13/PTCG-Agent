
def _iter_block_pairs(
    left: BlockManager, right: BlockManager
) -> Iterator[BlockPairInfo]:
    # At this point we have already checked the parent DataFrames for
    #  assert rframe._indexed_same(lframe)

    for blk in left.blocks:
        locs = blk.mgr_locs
        blk_vals = blk.values

        left_ea = blk_vals.ndim == 1

        rblks = right._slice_take_blocks_ax0(locs.indexer, only_slice=True)

        # Assertions are disabled for performance, but should hold:
        # if left_ea:
        #    assert len(locs) == 1, locs
        #    assert len(rblks) == 1, rblks
        #    assert rblks[0].shape[0] == 1, rblks[0].shape

        for rblk in rblks:
            right_ea = rblk.values.ndim == 1

            lvals, rvals = _get_same_shape_values(blk, rblk, left_ea, right_ea)
            info = BlockPairInfo(lvals, rvals, locs, left_ea, right_ea, rblk)
            yield info

