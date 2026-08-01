
def assert_allclose_cc(actual, desired, **kw):
    """Almost equal or complex conjugates almost equal"""
    try:
        assert_allclose(actual, desired, **kw)
    except AssertionError:
        assert_allclose(actual, conj(desired), **kw)

