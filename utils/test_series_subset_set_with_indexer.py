
def test_series_subset_set_with_indexer(backend, indexer_si, indexer):
    # Case: setting values in a viewing Series with an indexer
    _, _, Series = backend
    s = Series([1, 2, 3], index=["a", "b", "c"])
    s_orig = s.copy()
    subset = s[:]

    if (
        indexer_si is tm.setitem
        and isinstance(indexer, np.ndarray)
        and indexer.dtype.kind == "i"
    ):
        # In 3.0 we treat integers as always-labels
        with pytest.raises(KeyError):
            indexer_si(subset)[indexer] = 0
        return

    indexer_si(subset)[indexer] = 0
    expected = Series([0, 0, 3], index=["a", "b", "c"])
    tm.assert_series_equal(subset, expected)

    tm.assert_series_equal(s, s_orig)

