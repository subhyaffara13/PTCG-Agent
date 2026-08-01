
def test_stdlib_copy(dtype, string_list):
    arr = np.array(string_list, dtype=dtype)

    assert_array_equal(copy.copy(arr), arr)
    assert_array_equal(copy.deepcopy(arr), arr)

