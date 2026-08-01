
def test_numpy_to_float():
    from sympy.testing.pytest import skip
    from sympy.external import import_module
    np = import_module('numpy')
    if not np:
        skip('numpy not installed. Abort numpy tests.')

    def check_prec_and_relerr(npval, ratval):
        prec = np.finfo(npval).nmant + 1
        x = Float(npval)
        assert x._prec == prec
        y = Float(ratval, precision=prec)
        assert abs((x - y)/y) < 2**(-(prec + 1))

    check_prec_and_relerr(np.float16(2.0/3), Rational(2, 3))
    check_prec_and_relerr(np.float32(2.0/3), Rational(2, 3))
    check_prec_and_relerr(np.float64(2.0/3), Rational(2, 3))
    # extended precision, on some arch/compilers:
    x = np.longdouble(2)/3
    check_prec_and_relerr(x, Rational(2, 3))
    y = Float(x, precision=10)
    assert same_and_same_prec(y, Float(Rational(2, 3), precision=10))

    raises(TypeError, lambda: Float(np.complex64(1+2j)))
    raises(TypeError, lambda: Float(np.complex128(1+2j)))

