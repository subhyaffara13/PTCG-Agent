
def test_issue_7950():
    expr = And(Eq(x, 1), Eq(x, 2))
    assert simplify(expr) == S.false


def test_issue_7950():
    x = symbols('x', real=True)
    assert And(Eq(x, 1), Eq(x, 2)).simplify() == S.false

