
def create_block_manager_from_blocks(
    blocks: list[Block],
    axes: list[Index],
    consolidate: bool = True,
    verify_integrity: bool = True,
) -> BlockManager:
    # If verify_integrity=False, then caller is responsible for checking
    #  all(x.shape[-1] == len(axes[1]) for x in blocks)
    #  sum(x.shape[0] for x in blocks) == len(axes[0])
    #  set(x for blk in blocks for x in blk.mgr_locs) == set(range(len(axes[0])))
    #  all(blk.ndim == 2 for blk in blocks)
    # This allows us to safely pass verify_integrity=False

    try:
        mgr = BlockManager(blocks, axes, verify_integrity=verify_integrity)

    except ValueError as err:
        arrays = [blk.values for blk in blocks]
        tot_items = sum(arr.shape[0] for arr in arrays)
        raise_construction_error(tot_items, arrays[0].shape[1:], axes, err)

    if consolidate:
        mgr._consolidate_inplace()
    return mgr

