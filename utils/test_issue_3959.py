
def test_issue_3959():
    x, y = symbols('x, y')
    e = x*y
    assert e.subs(x, Matrix([3, 5, 3])) == Matrix([3, 5, 3])*y


def test_issue_3959():
    x, y = symbols('x, y')
    e = x*y
    assert e.subs(x, Matrix([3, 5, 3])) == Matrix([3, 5, 3])*y

