
def test_stack_timezone_aware_values(future_stack):
    # GH 19420
    ts = date_range(freq="D", start="20180101", end="20180103", tz="America/New_York")
    df = DataFrame({"A": ts}, index=["a", "b", "c"])
    result = df.stack(future_stack=future_stack)
    expected = Series(
        ts,
        index=MultiIndex(levels=[["a", "b", "c"], ["A"]], codes=[[0, 1, 2], [0, 0, 0]]),
    )
    tm.assert_series_equal(result, expected)

