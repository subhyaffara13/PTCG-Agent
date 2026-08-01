
def test_signsimp():
    e = x*(-x + 1) + x*(x - 1)
    assert signsimp(Eq(e, 0)) is S.true
    assert Abs(x - 1) == Abs(1 - x)
    assert signsimp(y - x) == y - x
    assert signsimp(y - x, evaluate=False) == Mul(-1, x - y, evaluate=False)

