
def _reset_block_mgr_locs(nbs: list[Block], locs) -> None:
    """
    Reset mgr_locs to correspond to our original DataFrame.
    """
    for nb in nbs:
        nblocs = locs[nb.mgr_locs.indexer]
        nb.mgr_locs = nblocs

