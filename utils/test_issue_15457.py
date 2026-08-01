
def test_issue_15457():
    x, a, b = symbols('x a b', real=True)
    definite = integrate(exp(Abs(x-2)), (x, a, b))
    indefinite = integrate(exp(Abs(x-2)), x)
    assert definite.subs({a: 1, b: 3}) == -2 + 2*E
    assert indefinite.subs(x, 3) - indefinite.subs(x, 1) == -2 + 2*E
    assert definite.subs({a: -3, b: -1}) == -exp(3) + exp(5)
    assert indefinite.subs(x, -1) - indefinite.subs(x, -3) == -exp(3) + exp(5)

