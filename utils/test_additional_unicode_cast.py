
def test_additional_unicode_cast(dtype):
    string_list = random_unicode_string_list()
    arr = np.array(string_list, dtype=dtype)
    # test that this short-circuits correctly
    assert_array_equal(arr, arr.astype(arr.dtype))
    # tests the casts via the comparison promoter
    assert_array_equal(arr, arr.astype(string_list.dtype))

