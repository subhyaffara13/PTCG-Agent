
def test_held_expression_UnevaluatedExpr():
    x = symbols("x")
    he = UnevaluatedExpr(1/x)
    e1 = x*he

    assert isinstance(e1, Mul)
    assert e1.args == (x, he)
    assert e1.doit() == 1
    assert UnevaluatedExpr(Derivative(x, x)).doit(deep=False
        ) == Derivative(x, x)
    assert UnevaluatedExpr(Derivative(x, x)).doit() == 1

    xx = Mul(x, x, evaluate=False)
    assert xx != x**2

    ue2 = UnevaluatedExpr(xx)
    assert isinstance(ue2, UnevaluatedExpr)
    assert ue2.args == (xx,)
    assert ue2.doit() == x**2
    assert ue2.doit(deep=False) == xx

    x2 = UnevaluatedExpr(2)*2
    assert type(x2) is Mul
    assert x2.args == (2, UnevaluatedExpr(2))

