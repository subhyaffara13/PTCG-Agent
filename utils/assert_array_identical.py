
def assert_array_identical(a, b):
    """Assert whether values AND type are the same"""
    assert_array_equal(a, b)
    assert_equal(a.dtype.type, b.dtype.type)

