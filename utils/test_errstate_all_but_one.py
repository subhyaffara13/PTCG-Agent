
def test_errstate_all_but_one():
    olderr = sc.geterr()
    with sc.errstate(all='raise', singular='ignore'):
        sc.gammaln(0)
        with assert_raises(sc.SpecialFunctionError):
            sc.spence(-1.0)
    assert_equal(olderr, sc.geterr())

