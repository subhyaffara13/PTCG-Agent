
def test_cummax_datetime():
    # GH 15561
    df = DataFrame({"a": [1], "b": pd.to_datetime(["2001"])})
    expected = Series(pd.to_datetime("2001"), index=[0], name="b")

    result = df.groupby("a")["b"].cummax()
    tm.assert_series_equal(expected, result)

