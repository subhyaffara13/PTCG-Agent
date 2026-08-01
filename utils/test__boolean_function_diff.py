
def test_BooleanFunction_diff():
    assert And(x, y).diff(x) == Piecewise((0, Eq(y, False)), (1, True))

