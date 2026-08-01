
def test_issue_17906():
    assert solveset(7**(x**2 - 80) - 49**x, x) == FiniteSet(-8, 10)

