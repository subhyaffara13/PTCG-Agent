
def test_issue_21908():
    assert nonlinsolve([(x**2 + 2*x - y**2)*exp(x), -2*y*exp(x)], x, y
                      ) == {(-2, 0), (0, 0)}

