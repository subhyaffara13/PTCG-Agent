
def test_issue_13651():
    expr = c + Mul(-1, a + b, evaluate=False)
    assert latex(expr) == r"c - \left(a + b\right)"


def test_issue_13651():
    expr1 = c + Mul(-1, a + b, evaluate=False)
    assert pretty(expr1) == 'c - (a + b)'
    expr2 = c + Mul(-1, a - b + d, evaluate=False)
    assert pretty(expr2) == 'c - (a - b + d)'

