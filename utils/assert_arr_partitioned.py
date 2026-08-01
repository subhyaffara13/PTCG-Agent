
def assert_arr_partitioned(kth, k, arr_part):
    assert_equal(arr_part[k], kth)
    assert_array_compare(operator.__le__, arr_part[:k], kth)
    assert_array_compare(operator.__ge__, arr_part[k:], kth)

