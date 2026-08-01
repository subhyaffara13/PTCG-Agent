
def test_Sum():
    e = Sum(z, (y, 0, x), (x, 0, 10))
    ref = 66*z
    assert e.doit() == ref
    assert lambdify([z], e)(7) == ref.subs(z, 7)


def test_Sum():
    assert mcode(Sum(sin(x), (x, 0, 10))) == "Hold[Sum[Sin[x], {x, 0, 10}]]"
    assert mcode(Sum(exp(-x**2 - y**2),
                     (x, -oo, oo),
                     (y, -oo, oo))) == \
        "Hold[Sum[Exp[-x^2 - y^2], {x, -Infinity, Infinity}, " \
        "{y, -Infinity, Infinity}]]"


def test_Sum():
    assert precedence(Sum(x, (x, y, y + 1))) == PRECEDENCE["Atom"]


def test_Sum():
    assert str(summation(cos(3*z), (z, x, y))) == "Sum(cos(3*z), (z, x, y))"
    assert str(Sum(x*y**2, (x, -2, 2), (y, -5, 5))) == \
        "Sum(x*y**2, (x, -2, 2), (y, -5, 5))"

