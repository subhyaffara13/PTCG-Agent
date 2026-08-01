
def test_dataframe_from_series_or_index_different_dtype(index_or_series):
    obj = index_or_series([1, 2], dtype="int64")
    df = DataFrame(obj, dtype="int32")
    assert not np.shares_memory(get_array(obj), get_array(df, 0))
    assert df._mgr._has_no_reference(0)

