
def test_asfreq_non_unique(unit):
    # GH #1077
    rng = date_range("1/1/2000", "2/29/2000").as_unit(unit)
    rng2 = rng.repeat(2).values
    ts = Series(np.random.default_rng(2).standard_normal(len(rng2)), index=rng2)

    msg = "cannot reindex on an axis with duplicate labels"
    with pytest.raises(ValueError, match=msg):
        ts.asfreq("B")

