
def test_UnevaluatedExpr():
    p, q, r = symbols("p q r", real=True)
    q_r = UnevaluatedExpr(q + r)
    expr = abs(exp(p+q_r))
    assert fcode(expr, source_format="free") == "exp(p + (q + r))"
    x, y, z = symbols("x y z")
    y_z = UnevaluatedExpr(y + z)
    expr2 = abs(exp(x+y_z))
    assert fcode(expr2, human=False)[2].lstrip() == "exp(re(x) + re(y + z))"
    assert fcode(expr2, user_functions={"re": "realpart"}).lstrip() == "exp(realpart(x) + realpart(y + z))"


def test_UnevaluatedExpr():
    a, b = symbols("a b")
    expr1 = 2*UnevaluatedExpr(a+b)
    assert str(expr1) == "2*(a + b)"

