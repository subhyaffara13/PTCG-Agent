
def test_issue_15024():
    function = (x + 5)/sqrt(-x**2 - 10*x)
    assert solveset(function, x, S.Reals) == FiniteSet(Integer(-5))

