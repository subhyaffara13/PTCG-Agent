
def test_errstate_cpp_basic():
    olderr = sc.geterr()
    with sc.errstate(underflow='raise'):
        with assert_raises(sc.SpecialFunctionError):
            sc.wrightomega(-1000)
    assert_equal(olderr, sc.geterr())

