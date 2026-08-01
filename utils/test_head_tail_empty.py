
def test_head_tail_empty():
    # test empty dataframe
    empty_df = DataFrame()
    tm.assert_frame_equal(empty_df.tail(), empty_df)
    tm.assert_frame_equal(empty_df.head(), empty_df)

