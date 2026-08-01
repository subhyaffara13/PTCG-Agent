
def test_complex_types(tp):
    """Check formatting of complex types.

        This is only for the str function, and only for simple types.
        The precision of np.float32 and np.longdouble aren't the same as the
        python float precision.

    """
    for x in [0, 1, -1, 1e20]:
        assert_equal(str(tp(x)), str(complex(x)),
                     err_msg=f'Failed str formatting for type {tp}')
        assert_equal(str(tp(x * 1j)), str(complex(x * 1j)),
                     err_msg=f'Failed str formatting for type {tp}')
        assert_equal(str(tp(x + x * 1j)), str(complex(x + x * 1j)),
                     err_msg=f'Failed str formatting for type {tp}')

    if tp(1e16).itemsize > 8:
        assert_equal(str(tp(1e16)), str(complex(1e16)),
                     err_msg=f'Failed str formatting for type {tp}')
    else:
        ref = '(1e+16+0j)'
        assert_equal(str(tp(1e16)), ref,
                     err_msg=f'Failed str formatting for type {tp}')

