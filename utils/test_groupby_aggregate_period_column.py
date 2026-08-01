
def test_groupby_aggregate_period_column(func):
    # GH 31471
    groups = [1, 2]
    periods = pd.period_range("2020", periods=2, freq="Y")
    df = DataFrame({"a": groups, "b": periods})

    result = getattr(df.groupby("a")["b"], func)()
    idx = pd.Index([1, 2], name="a")
    expected = Series(periods, index=idx, name="b")

    tm.assert_series_equal(result, expected)

