
def test_issue_9778():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert solveset(x**3 + 1, x, S.Reals) == FiniteSet(-1)
    assert solveset(x**Rational(3, 5) + 1, x, S.Reals) == S.EmptySet
    assert solveset(x**3 + y, x, S.Reals) == \
        FiniteSet(-Abs(y)**Rational(1, 3)*sign(y))

