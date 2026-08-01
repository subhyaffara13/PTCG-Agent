
def test_putmask_aligns_rhs_no_reference(dtype):
    df = DataFrame({"a": [1.5, 2], "b": 1.5}, dtype=dtype)
    arr_a = get_array(df, "a")
    df[df == df] = DataFrame({"a": [5.5, 5]})
    assert np.shares_memory(arr_a, get_array(df, "a"))

