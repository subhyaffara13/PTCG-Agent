
def test_agg_listlike_result():
    # GH-29587 user defined function returning list-likes
    df = DataFrame({"A": [2, 2, 3], "B": [1.5, np.nan, 1.5], "C": ["foo", None, "bar"]})

    def func(group_col):
        return list(group_col.dropna().unique())

    result = df.agg(func)
    expected = Series([[2, 3], [1.5], ["foo", "bar"]], index=["A", "B", "C"])
    tm.assert_series_equal(result, expected)

    result = df.agg([func])
    expected = expected.to_frame("func").T
    tm.assert_frame_equal(result, expected)

