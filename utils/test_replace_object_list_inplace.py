
def test_replace_object_list_inplace(value):
    df = DataFrame({"a": ["a", "b", "c"]}, dtype=object)
    arr = get_array(df, "a")
    df.replace(["c"], value, inplace=True)
    assert np.shares_memory(arr, get_array(df, "a"))
    assert df._mgr._has_no_reference(0)

