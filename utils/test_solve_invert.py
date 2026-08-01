
def test_solve_invert():
    assert solveset_real(exp(x) - 3, x) == FiniteSet(log(3))
    assert solveset_real(log(x) - 3, x) == FiniteSet(exp(3))

    assert solveset_real(3**(x + 2), x) == FiniteSet()
    assert solveset_real(3**(2 - x), x) == FiniteSet()

    assert solveset_real(y - b*exp(a/x), x) == Intersection(
        S.Reals, FiniteSet(a/log(y/b)))

    # issue 4504
    assert solveset_real(2**x - 10, x) == FiniteSet(1 + log(5)/log(2))

