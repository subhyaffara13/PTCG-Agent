
def test_issue_25738():
    assert reduce_inequalities(3 < abs(x)
        ) == reduce_inequalities(pi < abs(x)).subs(pi, 3)

