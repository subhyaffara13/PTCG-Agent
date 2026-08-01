
def test_errstate_c_basic():
    olderr = sc.geterr()
    with sc.errstate(domain='raise'):
        with assert_raises(sc.SpecialFunctionError):
            sc.spence(-1)
    assert_equal(olderr, sc.geterr())

