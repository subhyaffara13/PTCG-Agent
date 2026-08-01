
def test_min_count(func, min_count, value):
    # GH#37821
    df = DataFrame({"a": [1] * 3, "b": [1, np.nan, np.nan], "c": [np.nan] * 3})
    result = getattr(df.groupby("a"), func)(min_count=min_count)
    expected = DataFrame({"b": [value], "c": [np.nan]}, index=Index([1], name="a"))
    tm.assert_frame_equal(result, expected)

