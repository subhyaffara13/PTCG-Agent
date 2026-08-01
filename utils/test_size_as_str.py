
def test_size_as_str(how, axis):
    # GH 39934
    df = DataFrame(
        {"A": [None, 2, 3], "B": [1.0, np.nan, 3.0], "C": ["foo", None, "bar"]}
    )
    # Just a string attribute arg same as calling df.arg
    # on the columns
    result = getattr(df, how)("size", axis=axis)
    if axis in (0, "index"):
        expected = Series(df.shape[0], index=df.columns)
    else:
        expected = Series(df.shape[1], index=df.index)
    tm.assert_series_equal(result, expected)

