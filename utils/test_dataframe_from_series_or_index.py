
def test_dataframe_from_series_or_index(data, dtype, index_or_series):
    obj = index_or_series(data, dtype=dtype)
    obj_orig = obj.copy(deep=True)  # deep=True needed for Index

    # default is copy=False -> DataFrame holds a shallow copy of original Index/Series
    df = DataFrame(obj)
    assert tm.shares_memory(get_array(obj), get_array(df, 0))
    assert not df._mgr._has_no_reference(0)

    df.iloc[0, 0] = data[-1]
    tm.assert_equal(obj, obj_orig)

    # with passing the (identical) dtype -> same
    df = DataFrame(obj, dtype=dtype)
    assert tm.shares_memory(get_array(obj), get_array(df, 0))
    assert not df._mgr._has_no_reference(0)

    df.iloc[0, 0] = data[-1]
    tm.assert_equal(obj, obj_orig)

    # forcing copy=True still results in an actual hard copy up front
    df = DataFrame(obj, copy=True)
    if not (obj.dtype == "str" and obj.dtype.storage == "pyarrow"):
        # ArrowExtensionArray deep copy still points to the same underlying data
        assert not tm.shares_memory(get_array(obj), get_array(df, 0))
        assert df._mgr._has_no_reference(0)

    df.iloc[0, 0] = data[-1]
    tm.assert_equal(obj, obj_orig)

