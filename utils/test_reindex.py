
def test_reindex(datetime_series, string_series):
    identity = string_series.reindex(string_series.index)

    assert tm.shares_memory(string_series.index, identity.index)

    assert identity.index.is_(string_series.index)
    assert identity.index.identical(string_series.index)

    subIndex = string_series.index[10:20]
    subSeries = string_series.reindex(subIndex)

    for idx, val in subSeries.items():
        assert val == string_series[idx]

    subIndex2 = datetime_series.index[10:20]
    subTS = datetime_series.reindex(subIndex2)

    for idx, val in subTS.items():
        assert val == datetime_series[idx]
    stuffSeries = datetime_series.reindex(subIndex)

    assert np.isnan(stuffSeries).all()

    # This is extremely important for the Cython code to not screw up
    nonContigIndex = datetime_series.index[::2]
    subNonContig = datetime_series.reindex(nonContigIndex)
    for idx, val in subNonContig.items():
        assert val == datetime_series[idx]

    # return a copy the same index here
    result = datetime_series.reindex()
    assert result is not datetime_series


def test_reindex(idx):
    result, indexer = idx.reindex(list(idx[:4]))
    assert isinstance(result, MultiIndex)
    assert result.names == ["first", "second"]
    assert [level.name for level in result.levels] == ["first", "second"]

    result, indexer = idx.reindex(list(idx))
    assert isinstance(result, MultiIndex)
    assert indexer is None
    assert result.names == ["first", "second"]
    assert [level.name for level in result.levels] == ["first", "second"]

