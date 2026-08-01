
def test_issue_7110():
    y = -2*x**3 + 4*x**2 - 2*x + 5
    assert any(ask(Q.real(i)) for i in solve(y))

