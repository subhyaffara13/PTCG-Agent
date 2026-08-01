
def test_issue_14384():
    x, a = symbols('x a')
    assert series(x**a, x) == x**a
    assert series(x**(-2*a), x) == x**(-2*a)
    assert series(exp(a*log(x)), x) == exp(a*log(x))
    raises(PoleError, lambda: series(x**I, x))
    raises(PoleError, lambda: series(x**(I + 1), x))
    raises(PoleError, lambda: series(exp(I*log(x)), x))

