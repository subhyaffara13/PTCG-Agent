
def test_apply_iteration():
    # #2300
    N = 1000
    ind = date_range(start="2000-01-01", freq="D", periods=N)
    df = DataFrame({"open": 1, "close": 2}, index=ind)
    tg = Grouper(freq="ME")

    grouper, _ = tg._get_grouper(df)

    # Errors
    grouped = df.groupby(grouper, group_keys=False)

    def f(df):
        return df["close"] / df["open"]

    # it works!
    result = grouped.apply(f)
    tm.assert_index_equal(result.index, df.index)

