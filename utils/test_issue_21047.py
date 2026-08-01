
def test_issue_21047():
    f = (2 - x)**2 + (sqrt(x - 1) - 1)**6
    assert solveset(f, x, S.Reals) == FiniteSet(2)

    f = (sqrt(x)-1)**2 + (sqrt(x)+1)**2 -2*x**2 + sqrt(2)
    assert solveset(f, x, S.Reals) == FiniteSet(
        S.Half - sqrt(2*sqrt(2) + 5)/2, S.Half + sqrt(2*sqrt(2) + 5)/2)

