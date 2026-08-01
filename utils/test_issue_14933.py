
def test_issue_14933():
    x = Symbol('x')
    y = Symbol('y')

    inp = MatrixSymbol('inp', 1, 1)
    rep_dict = {y: inp[0, 0], x: inp[0, 0]}

    p = Piecewise((1, ITE(y > 0, x < 0, True)))
    assert p.xreplace(rep_dict) == Piecewise((1, ITE(inp[0, 0] > 0, inp[0, 0] < 0, True)))

