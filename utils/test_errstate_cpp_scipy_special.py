
def test_errstate_cpp_scipy_special():
    olderr = sc.geterr()
    with sc.errstate(singular='raise'):
        with assert_raises(sc.SpecialFunctionError):
            sc.lambertw(0, 1)
    assert_equal(olderr, sc.geterr())

