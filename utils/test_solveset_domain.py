
def test_solveset_domain():
    assert solveset(x**2 - x - 6, x, Interval(0, oo)) == FiniteSet(3)
    assert solveset(x**2 - 1, x, Interval(0, oo)) == FiniteSet(1)
    assert solveset(x**4 - 16, x, Interval(0, 10)) == FiniteSet(2)

