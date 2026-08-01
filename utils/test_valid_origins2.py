
def test_valid_origins2(xp, filter_func):
    """Regression test for #1311."""
    data = xp.asarray([1, 2, 3, 4, 5], dtype=xp.float64)

    # This should work, since for size == 3, the valid range for origin is
    # -1 to 1.
    list(filter_func(data, 3, origin=-1))
    list(filter_func(data, 3, origin=1))
    # Just check this raises an error instead of silently accepting or
    # segfaulting.
    assert_raises(ValueError, filter_func, data, 3, origin=2)

