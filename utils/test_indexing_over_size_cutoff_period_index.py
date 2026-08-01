
def test_indexing_over_size_cutoff_period_index(monkeypatch):
    # GH 27136

    monkeypatch.setattr(libindex, "_SIZE_CUTOFF", 1000)

    n = 1100
    idx = period_range("1/1/2000", freq="min", periods=n)
    assert idx._engine.over_size_threshold

    s = Series(np.random.default_rng(2).standard_normal(len(idx)), index=idx)

    pos = n - 1
    timestamp = idx[pos]
    assert timestamp in s.index

    # it works!
    s[timestamp]
    assert len(s.loc[[timestamp]]) > 0

