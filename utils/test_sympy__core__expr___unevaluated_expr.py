
def test_sympy__core__expr__UnevaluatedExpr():
    from sympy.core.expr import UnevaluatedExpr
    from sympy.abc import x
    assert _test_args(UnevaluatedExpr(x))

