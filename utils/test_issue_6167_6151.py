
def test_issue_6167_6151():
    n = pi**1000
    i = int(n)
    assert sign(n - i) == 1
    assert abs(n - i) == n - i
    x = Symbol('x')
    eps = pi**-1500
    big = pi**1000
    one = cos(x)**2 + sin(x)**2
    e = big*one - big + eps
    from sympy.simplify.simplify import simplify
    assert sign(simplify(e)) == 1
    for xi in (111, 11, 1, Rational(1, 10)):
        assert sign(e.subs(x, xi)) == 1

