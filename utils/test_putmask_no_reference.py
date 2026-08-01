
def test_putmask_no_reference(dtype):
    df = DataFrame({"a": [1, 2], "b": 1, "c": 2}, dtype=dtype)
    arr_a = get_array(df, "a")
    df[df == df] = 5
    assert np.shares_memory(arr_a, get_array(df, "a"))

