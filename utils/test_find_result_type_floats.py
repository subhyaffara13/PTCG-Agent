
def test_find_result_type_floats(right, result):
    left_dtype = np.dtype("float16")
    assert find_result_type(left_dtype, right) == result

