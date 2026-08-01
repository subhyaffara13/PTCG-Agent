
def test_downsample_non_unique(unit):
    rng = date_range("1/1/2000", "2/29/2000").as_unit(unit)
    rng2 = rng.repeat(5).values
    ts = Series(np.random.default_rng(2).standard_normal(len(rng2)), index=rng2)

    result = ts.resample("ME").mean()

    expected = ts.groupby(lambda x: x.month).mean()
    assert len(result) == 2
    tm.assert_almost_equal(result.iloc[0], expected[1])
    tm.assert_almost_equal(result.iloc[1], expected[2])

