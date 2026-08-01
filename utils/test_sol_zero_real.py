
def test_sol_zero_real():
    assert solveset_real(0, x) == S.Reals
    assert solveset(0, x, Interval(1, 2)) == Interval(1, 2)
    assert solveset_real(-x**2 - 2*x + (x + 1)**2 - 1, x) == S.Reals

