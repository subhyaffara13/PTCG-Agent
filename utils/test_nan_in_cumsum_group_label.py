
def test_nan_in_cumsum_group_label():
    # GH#58811
    df = DataFrame({"A": [1, None], "B": [2, 3]}, dtype="Int16")
    gb = df.groupby("A")["B"]
    result = gb.cumsum()
    expected = Series([2, None], dtype="Int16", name="B")
    tm.assert_series_equal(expected, result)

