
def _get_block_for_concat_plan(
    mgr: BlockManager, bp: BlockPlacement, blkno: int, *, max_len: int
) -> Block:
    blk = mgr.blocks[blkno]
    # Assertions disabled for performance:
    #  assert bp.is_slice_like
    #  assert blkno != -1
    #  assert (mgr.blknos[bp] == blkno).all()

    if len(bp) == len(blk.mgr_locs) and (
        blk.mgr_locs.is_slice_like and blk.mgr_locs.as_slice.step == 1
    ):
        nb = blk
    else:
        ax0_blk_indexer = mgr.blklocs[bp.indexer]

        slc = lib.maybe_indices_to_slice(ax0_blk_indexer, max_len)
        # TODO: in all extant test cases 2023-04-08 we have a slice here.
        #  Will this always be the case?
        if isinstance(slc, slice):
            nb = blk.slice_block_columns(slc)
        else:
            nb = blk.take_block_columns(slc)

    # assert nb.shape == (len(bp), mgr.shape[1])
    return nb

