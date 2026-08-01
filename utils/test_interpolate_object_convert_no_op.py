
def test_interpolate_object_convert_no_op():
    df = DataFrame({"a": ["a", "b", "c"], "b": 1})
    df["a"] = df["a"].astype(object)
    arr_a = get_array(df, "a")

    # Now CoW makes a copy, it should not!
    assert df._mgr._has_no_reference(0)
    assert np.shares_memory(arr_a, get_array(df, "a"))

