
def test_issue_13550():
    assert solveset(x**2 - 2*x - 15, symbol = x, domain = Interval(-oo, 0)) == FiniteSet(-3)

