
def test_errstate_pyx_basic():
    olderr = sc.geterr()
    with sc.errstate(singular='raise'):
        with assert_raises(sc.SpecialFunctionError):
            sc.loggamma(0)
    assert_equal(olderr, sc.geterr())

