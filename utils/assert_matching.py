
def assert_matching(actual, expected, check_dtype=False):
    # avoid specifying internal representation
    # as much as possible
    assert len(actual) == len(expected)
    for act, exp in zip(actual, expected, strict=True):
        act = np.asarray(act)
        exp = np.asarray(exp)
        tm.assert_numpy_array_equal(act, exp, check_dtype=check_dtype)

