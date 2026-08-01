
def test_aggregate_item_by_item(df):
    grouped = df.groupby("A")

    aggfun_0 = lambda ser: ser.size
    result = grouped.agg(aggfun_0)
    foosum = (df.A == "foo").sum()
    barsum = (df.A == "bar").sum()
    K = len(result.columns)

    # GH5782
    exp = Series(np.array([foosum] * K), index=list("BCD"), name="foo")
    tm.assert_series_equal(result.xs("foo"), exp)

    exp = Series(np.array([barsum] * K), index=list("BCD"), name="bar")
    tm.assert_almost_equal(result.xs("bar"), exp)

    def aggfun_1(ser):
        return ser.size

    result = DataFrame().groupby(df.A).agg(aggfun_1)
    assert isinstance(result, DataFrame)
    assert len(result) == 0

