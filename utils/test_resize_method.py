
def test_resize_method(string_list):
    sarr = np.array(string_list, dtype="T")
    sarr.resize(len(string_list) + 3)
    assert_array_equal(sarr, np.array(string_list + [''] * 3,  dtype="T"))

