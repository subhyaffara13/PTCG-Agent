
def test_issue_19484():
    assert simplify(sign(x) * Abs(x)) == x

    e = x + sign(x + x**3)
    assert simplify(Abs(x + x**3)*e) == x**3 + x*Abs(x**3 + x) + x

    e = x**2 + sign(x**3 + 1)
    assert simplify(Abs(x**3 + 1) * e) == x**3 + x**2*Abs(x**3 + 1) + 1

    f = Function('f')
    e = x + sign(x + f(x)**3)
    assert simplify(Abs(x + f(x)**3) * e) == x*Abs(x + f(x)**3) + x + f(x)**3

