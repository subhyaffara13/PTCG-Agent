
def test_resample_to_period_monthly_buglet(unit):
    # GH #1259

    rng = date_range("1/1/2000", "12/31/2000").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    result = ts.resample("ME").mean().to_period()
    exp_index = period_range("Jan-2000", "Dec-2000", freq="M")
    tm.assert_index_equal(result.index, exp_index)

