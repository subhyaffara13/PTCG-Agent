
def test_replace_empty_list():
    df = DataFrame({"a": [1, 2]})

    df2 = df.replace([], [])
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert not df._mgr._has_no_reference(0)
    arr_a = get_array(df, "a")
    df.replace([], [])
    assert np.shares_memory(get_array(df, "a"), arr_a)
    assert not df._mgr._has_no_reference(0)
    assert not df2._mgr._has_no_reference(0)

