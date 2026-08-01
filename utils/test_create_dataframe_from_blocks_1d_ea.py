
def test_create_dataframe_from_blocks_1dEA(array):
    # ExtensionArrays can be passed as 1D even if stored under the hood as 2D
    df = pd.DataFrame({"a": array})

    block = df._mgr.blocks[0]
    result = create_dataframe_from_blocks(
        [(block.values[0], block.mgr_locs.as_array)], index=df.index, columns=df.columns
    )
    tm.assert_frame_equal(result, df)

