
def test_consistency_for_boxed(box, int_frame_const_col):
    # passing an array or list should not affect the output shape
    df = int_frame_const_col

    result = df.apply(lambda x: box([1, 2]), axis=1)
    expected = Series([box([1, 2]) for t in df.itertuples()])
    tm.assert_series_equal(result, expected)

    result = df.apply(lambda x: box([1, 2]), axis=1, result_type="expand")
    expected = int_frame_const_col[["A", "B"]].rename(columns={"A": 0, "B": 1})
    tm.assert_frame_equal(result, expected)

