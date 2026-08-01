
def test_resample_upsample(unit):
    # from daily
    dti = date_range(
        start=datetime(2005, 1, 1), end=datetime(2005, 1, 10), freq="D", name="index"
    ).as_unit(unit)

    s = Series(np.random.default_rng(2).random(len(dti)), dti)

    # to minutely, by padding
    result = s.resample("Min").ffill()
    assert len(result) == 12961
    assert result.iloc[0] == s.iloc[0]
    assert result.iloc[-1] == s.iloc[-1]

    assert result.index.name == "index"

