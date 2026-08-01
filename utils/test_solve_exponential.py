
def test_solve_exponential():
    assert _solve_exponential(3**(2*x) - 2**(x + 3), 0, x, S.Reals) == \
        FiniteSet(-3*log(2)/(-2*log(3) + log(2)))
    assert _solve_exponential(2**y + 4**y, 1, y, S.Reals) == \
        FiniteSet(log(Rational(-1, 2) + sqrt(5)/2)/log(2))
    assert _solve_exponential(2**y + 4**y, 0, y, S.Reals) == \
        S.EmptySet
    assert _solve_exponential(2**x + 3**x - 5**x, 0, x, S.Reals) == \
        ConditionSet(x, Eq(2**x + 3**x - 5**x, 0), S.Reals)

