
def test_issue_15439():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    assert latex((x * y).subs(y, -y)) == r"x \left(- y\right)"
    assert latex((x * y).subs(y, -2*y)) == r"x \left(- 2 y\right)"
    assert latex((x * y).subs(x, -x)) == r"\left(- x\right) y"

