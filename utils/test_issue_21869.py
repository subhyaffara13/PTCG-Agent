
def test_issue_21869():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    expr = And(Eq(x**2, 4), Le(x, y))
    assert expr.simplify() == expr

    expr = And(Eq(x**2, 4), Eq(x, 2))
    assert expr.simplify() == Eq(x, 2)

    expr = And(Eq(x**3, x**2), Eq(x, 1))
    assert expr.simplify() == Eq(x, 1)

    expr = And(Eq(sin(x), x**2), Eq(x, 0))
    assert expr.simplify() == Eq(x, 0)

    expr = And(Eq(x**3, x**2), Eq(x, 2))
    assert expr.simplify() == S.false

    expr = And(Eq(y, x**2), Eq(x, 1))
    assert expr.simplify() == And(Eq(y,1), Eq(x, 1))

    expr = And(Eq(y**2, 1), Eq(y, x**2), Eq(x, 1))
    assert expr.simplify() == And(Eq(y,1), Eq(x, 1))

    expr = And(Eq(y**2, 4), Eq(y, 2*x**2), Eq(x, 1))
    assert expr.simplify() == And(Eq(y,2), Eq(x, 1))

    expr = And(Eq(y**2, 4), Eq(y, x**2), Eq(x, 1))
    assert expr.simplify() == S.false

