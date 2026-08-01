
def test_replace_list_multiple_elements_inplace():
    df = DataFrame({"a": [1, 2, 3]})
    arr = get_array(df, "a")
    df.replace([1, 2], 4, inplace=True)
    assert np.shares_memory(arr, get_array(df, "a"))
    assert df._mgr._has_no_reference(0)

