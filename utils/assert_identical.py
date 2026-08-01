
def assert_identical(a, b):
    """Assert whether value AND type are the same"""
    assert_equal(a, b)
    if isinstance(b, str):
        assert_equal(type(a), type(b))
    else:
        assert_equal(np.asarray(a).dtype.type, np.asarray(b).dtype.type)

