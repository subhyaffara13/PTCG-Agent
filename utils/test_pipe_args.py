
def test_pipe_args():
    # Test passing args to the pipe method of DataFrameGroupBy.
    # Issue #17871

    df = DataFrame(
        {
            "group": ["A", "A", "B", "B", "C"],
            "x": [1.0, 2.0, 3.0, 2.0, 5.0],
            "y": [10.0, 100.0, 1000.0, -100.0, -1000.0],
        }
    )

    def f(dfgb, arg1):
        filtered = dfgb.filter(lambda grp: grp.y.mean() > arg1, dropna=False)
        return filtered.groupby("group")

    def g(dfgb, arg2):
        return dfgb.sum() / dfgb.sum().sum() + arg2

    def h(df, arg3):
        return df.x + df.y - arg3

    result = df.groupby("group").pipe(f, 0).pipe(g, 10).pipe(h, 100)

    # Assert the results here
    index = Index(["A", "B"], name="group")
    expected = pd.Series([-79.5160891089, -78.4839108911], index=index)

    tm.assert_series_equal(result, expected)

    # test SeriesGroupby.pipe
    ser = pd.Series([1, 1, 2, 2, 3, 3])
    result = ser.groupby(ser).pipe(lambda grp: grp.sum() * grp.count())

    expected = pd.Series([4, 8, 12], index=Index([1, 2, 3], dtype=np.int64))

    tm.assert_series_equal(result, expected)

