
def test_issue_17604():
    lhs = -2**(3*x/11)*exp(x/11) + pi**(x/11)
    assert _is_exponential(lhs, x)
    assert _solve_exponential(lhs, 0, x, S.Complexes) == FiniteSet(0)

