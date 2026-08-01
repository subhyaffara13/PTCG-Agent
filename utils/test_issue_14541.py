
def test_issue_14541():
    solutions = solveset(sqrt(-x**2 - 2.0), x)
    assert abs(solutions.args[0]+1.4142135623731*I) <= 1e-9
    assert abs(solutions.args[1]-1.4142135623731*I) <= 1e-9

