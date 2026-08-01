
def assert_really_equal(x, y, rtol=None):
    """
    Sharper assertion function that is stricter about matching types, not just values

    This is useful/necessary in some cases:
      * dtypes for arrays that have the same _values_ (e.g. element 1.0 vs 1)
      * distinguishing complex from real NaN
      * result types for scalars

    We still want to be able to allow a relative tolerance for the values though.
    The main logic comparison logic is handled by the xp_assert_* functions.
    """
    def assert_func(x, y):
        xp_assert_equal(x, y) if rtol is None else xp_assert_close(x, y, rtol=rtol)

    def assert_complex_nan(x):
        assert np.isnan(x.real) and np.isnan(x.imag)

    assert type(x) is type(y), f"types not equal: {type(x)}, {type(y)}"

    # ensure we also compare the values _within_ an array appropriately,
    # e.g. assert_equal does not distinguish different complex nans in arrays
    if isinstance(x, np.ndarray):
        # assert_equal does not compare (all) types, only values
        assert x.dtype == y.dtype
        # for empty arrays resp. to ensure shapes match
        assert_func(x, y)
        for elem_x, elem_y in zip(x.ravel(), y.ravel()):
            assert_really_equal(elem_x, elem_y, rtol=rtol)
    elif np.isnan(x) and np.isnan(y) and _is_subdtype(type(x), "c"):
        assert_complex_nan(x) and assert_complex_nan(y)
    # no need to consider complex infinities due to numpy/numpy#25493
    else:
        assert_func(x, y)

