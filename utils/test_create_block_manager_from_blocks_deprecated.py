
def test_create_block_manager_from_blocks_deprecated():
    # GH#33892
    # If they must, downstream packages should get this from internals.api,
    #  not internals.
    msg = (
        "create_block_manager_from_blocks is deprecated and will be "
        "removed in a future version. Use public APIs instead"
    )
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        internals.create_block_manager_from_blocks

