
def test_agg_period_index():
    prng = period_range("2012-1-1", freq="M", periods=3)
    df = DataFrame(np.random.default_rng(2).standard_normal((3, 2)), index=prng)
    rs = df.groupby(level=0).sum()
    assert isinstance(rs.index, PeriodIndex)

    # GH 3579
    index = period_range(start="1999-01", periods=5, freq="M")
    s1 = Series(np.random.default_rng(2).random(len(index)), index=index)
    s2 = Series(np.random.default_rng(2).random(len(index)), index=index)
    df = DataFrame.from_dict({"s1": s1, "s2": s2})
    grouped = df.groupby(df.index.month)
    list(grouped)

