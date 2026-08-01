
def test_issue_22462():
    for de in [
            Eq(f(x).diff(x), -20*f(x)**2 - 500*f(x)/7200),
            Eq(f(x).diff(x), -2*f(x)**2 - 5*f(x)/7)]:
        assert 'Bernoulli' in classify_ode(de, f(x))


def test_issue_22462():
    x, f = symbols('x'), Function('f')
    n, Q = symbols('n Q', cls=Wild)
    pattern = -Q*f(x)**n
    eq = 5*f(x)**2
    assert pattern.matches(eq) == {n: 2, Q: -5}

