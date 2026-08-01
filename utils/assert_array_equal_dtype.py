
def assert_array_equal_dtype(x, y, **kwargs):
    assert_(x.dtype == y.dtype)
    assert_array_equal(x, y, **kwargs)

