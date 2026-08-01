
def test_DieDistribution():
    from sympy.abc import x
    X = DieDistribution(6)
    assert X.pmf(S.Half) is S.Zero
    assert X.pmf(x).subs({x: 1}).doit() == Rational(1, 6)
    assert X.pmf(x).subs({x: 7}).doit() == 0
    assert X.pmf(x).subs({x: -1}).doit() == 0
    assert X.pmf(x).subs({x: Rational(1, 3)}).doit() == 0
    raises(ValueError, lambda: X.pmf(Matrix([0, 0])))
    raises(ValueError, lambda: X.pmf(x**2 - 1))

