
def test_dataframe_from_dict_of_series(columns, index, dtype):
    # Case: constructing a DataFrame from Series objects with copy=False
    # has to do a lazy following CoW rules
    # (the default for DataFrame(dict) is still to copy to ensure consolidation)
    s1 = Series([1, 2, 3])
    s2 = Series([4, 5, 6])
    s1_orig = s1.copy()
    expected = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6]}, index=index, columns=columns, dtype=dtype
    )

    result = DataFrame(
        {"a": s1, "b": s2}, index=index, columns=columns, dtype=dtype, copy=False
    )

    # the shallow copy still shares memory
    assert np.shares_memory(get_array(result, "a"), get_array(s1))

    # mutating the new dataframe doesn't mutate original
    result.iloc[0, 0] = 10
    assert not np.shares_memory(get_array(result, "a"), get_array(s1))
    tm.assert_series_equal(s1, s1_orig)

    # the same when modifying the parent series
    s1 = Series([1, 2, 3])
    s2 = Series([4, 5, 6])
    result = DataFrame(
        {"a": s1, "b": s2}, index=index, columns=columns, dtype=dtype, copy=False
    )
    s1.iloc[0] = 10
    assert not np.shares_memory(get_array(result, "a"), get_array(s1))
    tm.assert_frame_equal(result, expected)

