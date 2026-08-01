
def test_Mul_does_not_cancel_infinities():
    a, b = symbols('a b')
    assert ((zoo + 3*a)/(3*a + zoo)) is nan
    assert ((b - oo)/(b - oo)) is nan
    # issue 13904
    expr = (1/(a+b) + 1/(a-b))/(1/(a+b) - 1/(a-b))
    assert expr.subs(b, a) is nan

