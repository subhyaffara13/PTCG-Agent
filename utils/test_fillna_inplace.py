
def test_fillna_inplace():
    df = DataFrame({"a": [1.5, np.nan], "b": 1})
    arr_a = get_array(df, "a")
    arr_b = get_array(df, "b")

    df.fillna(5.5, inplace=True)
    assert np.shares_memory(get_array(df, "a"), arr_a)
    assert np.shares_memory(get_array(df, "b"), arr_b)
    assert df._mgr._has_no_reference(0)
    assert df._mgr._has_no_reference(1)

