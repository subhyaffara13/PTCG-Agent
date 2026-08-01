
def test_arg_leading_term_and_series():
    x = Symbol('x')
    assert arg(x).as_leading_term(x, cdir = 1) == 0
    assert arg(x).as_leading_term(x, cdir = -1) == pi
    raises(PoleError, lambda: arg(x + I).as_leading_term(x, cdir = 1))
    raises(PoleError, lambda: arg(2*x).as_leading_term(x, cdir = I))

    assert arg(x).nseries(x) == 0
    assert arg(x).nseries(x, n=0) == Order(1)

