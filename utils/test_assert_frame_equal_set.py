
def test_assert_frame_equal_set():
    # GH#51727
    df1 = DataFrame({"set_column": [{1, 2, 3}, {4, 5, 6}]})
    df2 = DataFrame({"set_column": [{1, 2, 3}, {4, 5, 6}]})
    tm.assert_frame_equal(df1, df2)

