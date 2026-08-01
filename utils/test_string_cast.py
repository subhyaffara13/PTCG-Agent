
def test_string_cast():
    str_arr = np.array(["1234", "1234\0\0"], dtype='S')
    uni_arr1 = str_arr.astype('>U')
    uni_arr2 = str_arr.astype('<U')

    assert_array_equal(str_arr != uni_arr1, np.ones(2, dtype=bool))
    assert_array_equal(uni_arr1 != str_arr, np.ones(2, dtype=bool))
    assert_array_equal(str_arr == uni_arr1, np.zeros(2, dtype=bool))
    assert_array_equal(uni_arr1 == str_arr, np.zeros(2, dtype=bool))

    assert_array_equal(uni_arr1, uni_arr2)

