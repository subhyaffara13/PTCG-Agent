
def test_rolling_apply_with_pandas_objects(window):
    # 5071
    df = DataFrame(
        {
            "A": np.random.default_rng(2).standard_normal(5),
            "B": np.random.default_rng(2).integers(0, 10, size=5),
        },
        index=date_range("20130101", periods=5, freq="s"),
    )

    # we have an equal spaced timeseries index
    # so simulate removing the first period
    def f(x):
        if x.index[0] == df.index[0]:
            return np.nan
        return x.iloc[-1]

    result = df.rolling(window).apply(f, raw=False)
    expected = df.iloc[2:].reindex_like(df)
    tm.assert_frame_equal(result, expected)

    with tm.external_error_raised(AttributeError):
        df.rolling(window).apply(f, raw=True)

