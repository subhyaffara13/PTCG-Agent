
def test_indexer_caching(monkeypatch):
    # GH5727
    # make sure that indexers are in the _internal_names_set
    size_cutoff = 20
    with monkeypatch.context():
        monkeypatch.setattr(libindex, "_SIZE_CUTOFF", size_cutoff)
        index = MultiIndex.from_arrays([np.arange(size_cutoff), np.arange(size_cutoff)])
        s = Series(np.zeros(size_cutoff), index=index)

        # setitem
        s[s == 0] = 1
    expected = Series(np.ones(size_cutoff), index=index)
    tm.assert_series_equal(s, expected)

