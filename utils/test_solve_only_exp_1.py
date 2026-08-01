
def test_solve_only_exp_1():
    y = Symbol('y', positive=True)
    assert solveset_real(exp(x) - y, x) == FiniteSet(log(y))
    assert solveset_real(exp(x) + exp(-x) - 4, x) == \
        FiniteSet(log(-sqrt(3) + 2), log(sqrt(3) + 2))
    assert solveset_real(exp(x) + exp(-x) - y, x) != S.EmptySet

