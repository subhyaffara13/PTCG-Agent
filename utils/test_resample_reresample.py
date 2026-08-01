
def test_resample_reresample(unit):
    dti = date_range(
        start=datetime(2005, 1, 1), end=datetime(2005, 1, 10), freq="D"
    ).as_unit(unit)
    s = Series(np.random.default_rng(2).random(len(dti)), dti)
    bs = s.resample("B", closed="right", label="right").mean()
    result = bs.resample("8h").mean()
    assert len(result) == 25
    assert isinstance(result.index.freq, offsets.DateOffset)
    assert result.index.freq == offsets.Hour(8)

