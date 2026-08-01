
def assert_block_lengths(x):
    assert len(x) == len(x._mgr.blocks[0].mgr_locs)
    return 0

