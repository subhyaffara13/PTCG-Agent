
def _is_homogeneous_mgr(mgr: BlockManager, first_dtype: DtypeObj) -> bool:
    """
    Check if this Manager can be treated as a single ndarray.
    """
    if mgr.nblocks != 1:
        return False
    blk = mgr.blocks[0]
    if not (blk.mgr_locs.is_slice_like and blk.mgr_locs.as_slice.step == 1):
        return False

    return blk.dtype == first_dtype

