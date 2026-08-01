
def test_replace_inplace(to_replace):
    df = DataFrame({"a": [1.5, 2, 3]})
    arr_a = get_array(df, "a")
    df.replace(to_replace=1.5, value=15.5, inplace=True)

    assert np.shares_memory(get_array(df, "a"), arr_a)
    assert df._mgr._has_no_reference(0)

