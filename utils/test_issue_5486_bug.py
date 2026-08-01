
def test_issue_5486_bug():
    from sympy.core.expr import Expr
    from sympy.core.numbers import I
    assert abs(Expr._from_mpmath(I._to_mpmath(15), 15) - I) < 1.0e-15

