
def test_reindex_int(datetime_series):
    ts = datetime_series[::2]
    int_ts = Series(np.zeros(len(ts), dtype=int), index=ts.index)

    # this should work fine
    reindexed_int = int_ts.reindex(datetime_series.index)

    # if NaNs introduced
    assert reindexed_int.dtype == np.float64

    # NO NaNs introduced
    reindexed_int = int_ts.reindex(int_ts.index[::2])
    assert reindexed_int.dtype == np.dtype(int)

