
def test_literal_evalf_is_number_is_zero_is_comparable():
    x = symbols('x')
    f = Function('f')

    # issue 5033
    assert f.is_number is False
    # issue 6646
    assert f(1).is_number is False
    i = Integral(0, (x, x, x))
    # expressions that are symbolically 0 can be difficult to prove
    # so in case there is some easy way to know if something is 0
    # it should appear in the is_zero property for that object;
    # if is_zero is true evalf should always be able to compute that
    # zero
    assert i.n() == 0
    assert i.is_zero
    assert i.is_number is False
    assert i.evalf(2, strict=False) == 0

    # issue 10268
    n = sin(1)**2 + cos(1)**2 - 1
    assert n.is_comparable is False
    assert n.n(2).is_comparable is False
    assert n.n(2).n(2).is_comparable

