
def test_float_type_print(tp):
    """Check formatting when using print """
    for x in [0, 1, -1, 1e20]:
        _test_redirected_print(float(x), tp)

    for x in [np.inf, -np.inf, np.nan]:
        _test_redirected_print(float(x), tp, _REF[x])

    if tp(1e16).itemsize > 4:
        _test_redirected_print(1e16, tp)
    else:
        ref = '1e+16'
        _test_redirected_print(1e16, tp, ref)

