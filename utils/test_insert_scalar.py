
def test_insert_scalar(dtype, string_list):
    """Test that inserting a scalar works."""
    arr = np.array(string_list, dtype=dtype)
    scalar_instance = "what"
    arr[1] = scalar_instance
    assert_array_equal(
        arr,
        np.array(string_list[:1] + ["what"] + string_list[2:], dtype=dtype),
    )

