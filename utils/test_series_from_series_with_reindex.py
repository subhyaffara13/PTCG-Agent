
def test_series_from_series_with_reindex():
    # Case: constructing a Series from another Series with specifying an index
    # that potentially requires a reindex of the values
    ser = Series([1, 2, 3], name="name")

    # passing an index that doesn't actually require a reindex of the values
    # -> still getting a CoW shallow copy
    for index in [
        ser.index,
        ser.index.copy(),
        list(ser.index),
        ser.index.rename("idx"),
    ]:
        result = Series(ser, index=index)
        assert np.shares_memory(ser.values, result.values)
        result.iloc[0] = 0
        assert ser.iloc[0] == 1

        # forcing copy=True still results in an actual hard copy up front
        result = Series(ser, index=index, copy=True)
        assert not np.shares_memory(ser.values, result.values)
        assert not result._mgr.blocks[0].refs.has_reference()

    # ensure that if an actual reindex is needed, we don't have any refs
    # (mutating the result wouldn't trigger CoW)
    result = Series(ser, index=[0, 1, 2, 3])
    assert not np.shares_memory(ser.values, result.values)
    assert not result._mgr.blocks[0].refs.has_reference()

