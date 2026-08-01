
def _assert_almost_equal_both(a, b, **kwargs):
    """
    Check that two objects are approximately equal.

    This check is performed commutatively.

    Parameters
    ----------
    a : object
        The first object to compare.
    b : object
        The second object to compare.
    **kwargs
        The arguments passed to `tm.assert_almost_equal`.
    """
    tm.assert_almost_equal(a, b, **kwargs)
    tm.assert_almost_equal(b, a, **kwargs)

