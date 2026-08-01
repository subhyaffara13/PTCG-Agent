
def test_series_from_series(dtype):
    # Case: constructing a Series from another Series object follows CoW rules:
    # a new object is returned and thus mutations are not propagated
    ser = Series([1, 2, 3], name="name")

    # default is copy=False -> new Series is a shallow copy / view of original
    result = Series(ser, dtype=dtype)

    # the shallow copy still shares memory
    assert np.shares_memory(get_array(ser), get_array(result))

    assert result._mgr.blocks[0].refs.has_reference()

    # mutating new series copy doesn't mutate original
    result.iloc[0] = 0
    assert ser.iloc[0] == 1
    # mutating triggered a copy-on-write -> no longer shares memory
    assert not np.shares_memory(get_array(ser), get_array(result))

    # the same when modifying the parent
    result = Series(ser, dtype=dtype)

    # mutating original doesn't mutate new series
    ser.iloc[0] = 0
    assert result.iloc[0] == 1

    # forcing copy=False still gives a CoW shallow copy
    result = Series(ser, dtype=dtype, copy=False)
    assert np.shares_memory(get_array(ser), get_array(result))
    assert result._mgr.blocks[0].refs.has_reference()

    # forcing copy=True still results in an actual hard copy up front
    result = Series(ser, dtype=dtype, copy=True)
    assert not np.shares_memory(get_array(ser), get_array(result))
    assert ser._mgr._has_no_reference(0)

