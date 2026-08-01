
def test_groupby_none_column_name(using_infer_string):
    # GH#47348
    df = DataFrame({None: [1, 1, 2, 2], "b": [1, 1, 2, 3], "c": [4, 5, 6, 7]})
    by = [np.nan] if using_infer_string else [None]
    gb = df.groupby(by=by)
    result = gb.sum()
    expected = DataFrame({"b": [2, 5], "c": [9, 13]}, index=Index([1, 2], name=by[0]))
    tm.assert_frame_equal(result, expected)

