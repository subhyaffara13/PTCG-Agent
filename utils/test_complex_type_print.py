
def test_complex_type_print(tp):
    """Check formatting when using print """
    # We do not create complex with inf/nan directly because the feature is
    # missing in python < 2.6
    for x in [0, 1, -1, 1e20]:
        _test_redirected_print(complex(x), tp)

    if tp(1e16).itemsize > 8:
        _test_redirected_print(complex(1e16), tp)
    else:
        ref = '(1e+16+0j)'
        _test_redirected_print(complex(1e16), tp, ref)

    _test_redirected_print(complex(np.inf, 1), tp, '(inf+1j)')
    _test_redirected_print(complex(-np.inf, 1), tp, '(-inf+1j)')
    _test_redirected_print(complex(-np.nan, 1), tp, '(nan+1j)')

