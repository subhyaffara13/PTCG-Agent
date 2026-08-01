
def test_solve_only_exp_2():
    assert solveset_real(sqrt(exp(x)) + sqrt(exp(-x)) - 4, x) == \
        FiniteSet(2*log(-sqrt(3) + 2), 2*log(sqrt(3) + 2))

