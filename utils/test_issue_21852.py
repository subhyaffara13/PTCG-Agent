
def test_issue_21852():
    solution = [21 - 21*sqrt(2)/2]
    assert solve(2*x + sqrt(2*x**2) - 21) == solution

