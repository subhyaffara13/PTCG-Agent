
def test_issue_13849():
    t = symbols('t')
    assert solve((t*(sqrt(5) + sqrt(2)) - sqrt(2), t), t) == []


def test_issue_13849():
    assert nonlinsolve((t*(sqrt(5) + sqrt(2)) - sqrt(2), t), t) is S.EmptySet

