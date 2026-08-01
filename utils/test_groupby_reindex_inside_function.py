
def test_groupby_reindex_inside_function():
    periods = 1000
    ind = date_range(start="2012/1/1", freq="5min", periods=periods)
    df = DataFrame({"high": np.arange(periods), "low": np.arange(periods)}, index=ind)

    def agg_before(func, fix=False):
        """
        Run an aggregate func on the subset of data.
        """

        def _func(data):
            d = data.loc[data.index.map(lambda x: x.hour < 11)].dropna()
            if fix:
                data[data.index[0]]
            if len(d) == 0:
                return None
            return func(d)

        return _func

    grouped = df.groupby(lambda x: datetime(x.year, x.month, x.day))
    closure_bad = grouped.agg({"high": agg_before(np.max)})
    closure_good = grouped.agg({"high": agg_before(np.max, True)})

    tm.assert_frame_equal(closure_bad, closure_good)

