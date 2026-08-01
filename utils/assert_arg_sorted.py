
def assert_arg_sorted(arr, arg):
    # resulting array should be sorted and arg values should be unique
    assert_equal(arr[arg], np.sort(arr))
    assert_equal(np.sort(arg), np.arange(len(arg)))

