
def test_sympify_numpy():
    if not numpy:
        skip('numpy not installed. Abort numpy tests.')
    np = numpy

    def equal(x, y):
        return x == y and type(x) == type(y)

    assert sympify(np.bool_(1)) is S(True)
    try:
        assert equal(
            sympify(np.int_(1234567891234567891)), S(1234567891234567891))
        assert equal(
            sympify(np.intp(1234567891234567891)), S(1234567891234567891))
    except OverflowError:
        # May fail on 32-bit systems: Python int too large to convert to C long
        pass
    assert equal(sympify(np.intc(1234567891)), S(1234567891))
    assert equal(sympify(np.int8(-123)), S(-123))
    assert equal(sympify(np.int16(-12345)), S(-12345))
    assert equal(sympify(np.int32(-1234567891)), S(-1234567891))
    assert equal(
        sympify(np.int64(-1234567891234567891)), S(-1234567891234567891))
    assert equal(sympify(np.uint8(123)), S(123))
    assert equal(sympify(np.uint16(12345)), S(12345))
    assert equal(sympify(np.uint32(1234567891)), S(1234567891))
    assert equal(
        sympify(np.uint64(1234567891234567891)), S(1234567891234567891))
    assert equal(sympify(np.float32(1.123456)), Float(1.123456, precision=24))
    assert equal(sympify(np.float64(1.1234567891234)),
                Float(1.1234567891234, precision=53))

    # The exact precision of np.longdouble, npfloat128 and other extended
    # precision dtypes is platform dependent.
    ldprec = np.finfo(np.longdouble(1)).nmant + 1
    assert equal(sympify(np.longdouble(1.123456789)),
                 Float(1.123456789, precision=ldprec))

    assert equal(sympify(np.complex64(1 + 2j)), S(1.0 + 2.0*I))
    assert equal(sympify(np.complex128(1 + 2j)), S(1.0 + 2.0*I))

    lcprec = np.finfo(np.clongdouble(1)).nmant + 1
    assert equal(sympify(np.clongdouble(1 + 2j)),
                Float(1.0, precision=lcprec) + Float(2.0, precision=lcprec)*I)

    #float96 does not exist on all platforms
    if hasattr(np, 'float96'):
        f96prec = np.finfo(np.float96(1)).nmant + 1
        assert equal(sympify(np.float96(1.123456789)),
                    Float(1.123456789, precision=f96prec))

    #float128 does not exist on all platforms
    if hasattr(np, 'float128'):
        f128prec = np.finfo(np.float128(1)).nmant + 1
        assert equal(sympify(np.float128(1.123456789123)),
                    Float(1.123456789123, precision=f128prec))

