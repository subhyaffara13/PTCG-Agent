
def test_create_dataframe_from_blocks(float_frame):
    block = float_frame._mgr.blocks[0]
    index = float_frame.index.copy()
    columns = float_frame.columns.copy()

    result = create_dataframe_from_blocks(
        [(block.values, block.mgr_locs.as_array)], index=index, columns=columns
    )
    tm.assert_frame_equal(result, float_frame)

