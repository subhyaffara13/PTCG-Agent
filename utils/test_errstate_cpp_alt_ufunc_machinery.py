
def test_errstate_cpp_alt_ufunc_machinery():
    olderr = sc.geterr()
    with sc.errstate(singular='raise'):
        with assert_raises(sc.SpecialFunctionError):
            sc.gammaln(0)
    assert_equal(olderr, sc.geterr())

