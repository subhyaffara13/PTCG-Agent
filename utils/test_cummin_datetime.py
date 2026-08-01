
def test_cummin_datetime():
    # GH 15561
    df = DataFrame({"a": [1], "b": pd.to_datetime(["2001"])})
    expected = Series(pd.to_datetime("2001"), index=[0], name="b")

    result = df.groupby("a")["b"].cummin()
    tm.assert_series_equal(expected, result)

