
def test_groupby_aggregate_period_frame(func):
    # GH 31471
    groups = [1, 2]
    periods = pd.period_range("2020", periods=2, freq="Y")
    df = DataFrame({"a": groups, "b": periods})

    result = getattr(df.groupby("a"), func)()
    idx = pd.Index([1, 2], name="a")
    expected = DataFrame({"b": periods}, index=idx)

    tm.assert_frame_equal(result, expected)

