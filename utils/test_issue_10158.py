
def test_issue_10158():
    dom = S.Reals
    assert solveset(x*Max(x, 15) - 10, x, dom) == FiniteSet(Rational(2, 3))
    assert solveset(x*Min(x, 15) - 10, x, dom) == FiniteSet(-sqrt(10), sqrt(10))
    assert solveset(Max(Abs(x - 3) - 1, x + 2) - 3, x, dom) == FiniteSet(-1, 1)
    assert solveset(Abs(x - 1) - Abs(y), x, dom) == FiniteSet(-Abs(y) + 1, Abs(y) + 1)
    assert solveset(Abs(x + 4*Abs(x + 1)), x, dom) == FiniteSet(Rational(-4, 3), Rational(-4, 5))
    assert solveset(2*Abs(x + Abs(x + Max(3, x))) - 2, x, S.Reals) == FiniteSet(-1, -2)
    dom = S.Complexes
    raises(ValueError, lambda: solveset(x*Max(x, 15) - 10, x, dom))
    raises(ValueError, lambda: solveset(x*Min(x, 15) - 10, x, dom))
    raises(ValueError, lambda: solveset(Max(Abs(x - 3) - 1, x + 2) - 3, x, dom))
    raises(ValueError, lambda: solveset(Abs(x - 1) - Abs(y), x, dom))
    raises(ValueError, lambda: solveset(Abs(x + 4*Abs(x + 1)), x, dom))

