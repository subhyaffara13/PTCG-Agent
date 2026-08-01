
def test_expand_frac():
    assert expand((x + y)*y/x/(x + 1), frac=True) == \
        (x*y + y**2)/(x**2 + x)
    assert expand((x + y)*y/x/(x + 1), numer=True) == \
        (x*y + y**2)/(x*(x + 1))
    assert expand((x + y)*y/x/(x + 1), denom=True) == \
        y*(x + y)/(x**2 + x)
    eq = (x + 1)**2/y
    assert expand_numer(eq, multinomial=False) == eq
    # issue 26329
    eq = (exp(x*z) - exp(y*z))/exp(z*(x + y))
    ans = exp(-y*z) - exp(-x*z)
    assert eq.expand(numer=True) != ans
    assert eq.expand(numer=True, exact=True) == ans
    assert expand_numer(eq) != ans
    assert expand_numer(eq, exact=True) == ans

