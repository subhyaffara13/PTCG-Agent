
def test_longdouble_from_int(int_val):
    # for issue gh-9968
    str_val = str(int_val)
    # we'll expect a RuntimeWarning on platforms
    # with np.longdouble equivalent to np.double
    # for large integer input
    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings('always', '', RuntimeWarning)
        # can be inf==inf on some platforms
        assert np.longdouble(int_val) == np.longdouble(str_val)
        # we can't directly compare the int and
        # max longdouble value on all platforms
        if np.allclose(np.finfo(np.longdouble).max,
                       np.finfo(np.double).max) and w:
            assert w[0].category is RuntimeWarning

