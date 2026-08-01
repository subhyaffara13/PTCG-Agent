
def test_hasnans_uncached_for_series():
    # GH#19700
    # set float64 dtype to avoid upcast when setting nan
    idx = Index([0, 1], dtype="float64")
    assert idx.hasnans is False
    assert "hasnans" in idx._cache
    ser = idx.to_series()
    assert ser.hasnans is False
    assert not hasattr(ser, "_cache")
    ser.iloc[-1] = np.nan
    assert ser.hasnans is True

