
def test_find_result_type_uint_int(right, result):
    left_dtype = np.dtype("uint8")
    assert find_result_type(left_dtype, right) == result

