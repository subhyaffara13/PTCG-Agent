
def test_find_result_type_int_int(right, result):
    left_dtype = np.dtype("int8")
    assert find_result_type(left_dtype, right) == result

