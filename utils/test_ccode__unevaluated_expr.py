
def test_ccode_UnevaluatedExpr():
    assert ccode(UnevaluatedExpr(y * x) + z) == "z + x*y"
    assert ccode(UnevaluatedExpr(y + x) + z) == "z + (x + y)"  # gh-21955
    w = symbols('w')
    assert ccode(UnevaluatedExpr(y + x) + UnevaluatedExpr(z + w)) == "(w + z) + (x + y)"

    p, q, r = symbols("p q r", real=True)
    q_r = UnevaluatedExpr(q + r)
    expr = abs(exp(p+q_r))
    assert ccode(expr) == "exp(p + (q + r))"

