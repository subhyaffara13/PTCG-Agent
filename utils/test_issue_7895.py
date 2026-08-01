
def test_issue_7895():
    r = symbols('r', real=True)
    assert solve(sqrt(r) - 2) == [4]

