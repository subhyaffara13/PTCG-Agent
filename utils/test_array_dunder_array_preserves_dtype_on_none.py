
def test_array_dunder_array_preserves_dtype_on_none(dtype):
    """
    Regression test for: https://github.com/numpy/numpy/issues/27407
    Ensure that __array__(None) returns an array of the same dtype.
    """
    a = np.array([1], dtype=dtype)
    b = a.__array__(None)
    assert_array_equal(a, b, strict=True)

