
def test_dataframe_from_dict_of_series_with_dtype(index):
    # Variant of above, but now passing a dtype that causes a copy
    # -> need to ensure the result doesn't have refs set up to unnecessarily
    # trigger a copy on write
    s1 = Series([1.0, 2.0, 3.0])
    s2 = Series([4, 5, 6])
    df = DataFrame({"a": s1, "b": s2}, index=index, dtype="int64", copy=False)

    # df should own its memory, so mutating shouldn't trigger a copy
    arr_before = get_array(df, "a")
    assert not np.shares_memory(arr_before, get_array(s1))
    df.iloc[0, 0] = 100
    arr_after = get_array(df, "a")
    assert np.shares_memory(arr_before, arr_after)

