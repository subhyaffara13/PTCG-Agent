
def test_nth4():
    # doc example
    df = DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=["A", "B"])
    gb = df.groupby("A")
    result = gb.B.nth(0, dropna="all")
    expected = df.B.iloc[[1, 2]]
    tm.assert_series_equal(result, expected)

