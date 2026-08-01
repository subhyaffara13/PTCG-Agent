
def test_float_types(tp):
    """ Check formatting.

        This is only for the str function, and only for simple types.
        The precision of np.float32 and np.longdouble aren't the same as the
        python float precision.

    """
    for x in [0, 1, -1, 1e20]:
        assert_equal(str(tp(x)), str(float(x)),
                     err_msg=f'Failed str formatting for type {tp}')

    if tp(1e16).itemsize > 4:
        assert_equal(str(tp(1e16)), str(float('1e16')),
                     err_msg=f'Failed str formatting for type {tp}')
    else:
        ref = '1e+16'
        assert_equal(str(tp(1e16)), ref,
                     err_msg=f'Failed str formatting for type {tp}')

