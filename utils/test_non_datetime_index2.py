
def test_non_datetime_index2():
    rng = DatetimeIndex(["1/31/2000", "1/31/2001", "1/31/2002"])
    vals = rng.to_pydatetime()

    result = frequencies.infer_freq(vals)
    assert result == rng.inferred_freq

