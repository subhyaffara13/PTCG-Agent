
def assert_array_dicts_equal(left, right):
    for k, v in left.items():
        tm.assert_numpy_array_equal(np.asarray(v), np.asarray(right[k]))

