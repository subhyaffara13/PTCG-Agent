
def test_issue_6752():
    assert solve([a**2 + a, a - b], [a, b]) == [(-1, -1), (0, 0)]
    assert solve([a**2 + a*c, a - b], [a, b]) == [(0, 0), (-c, -c)]


def test_issue_6752():
    a, b = symbols('a, b', real=True)
    assert nonlinsolve([a**2 + a, a - b], [a, b]) == {(-1, -1), (0, 0)}

