
def test_issue_13890():
    x = Symbol("x")
    e = (-x/4 - S.One/12)**x - 1
    f = simplify(e)
    a = Rational(9, 5)
    assert abs(e.subs(x,a).evalf() - f.subs(x,a).evalf()) < 1e-15

