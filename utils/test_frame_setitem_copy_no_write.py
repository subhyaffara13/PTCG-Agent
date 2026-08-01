
def test_frame_setitem_copy_no_write(multiindex_dataframe_random_data):
    frame = multiindex_dataframe_random_data.T
    expected = frame
    df = frame.copy()
    with tm.raises_chained_assignment_error():
        df["foo"]["one"] = 2

    tm.assert_frame_equal(df, expected)

