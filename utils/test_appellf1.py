
def test_appellf1():
    a, b1, b2, c, x, y = symbols('a b1 b2 c x y')
    assert appellf1(a, b2, b1, c, y, x) == appellf1(a, b1, b2, c, x, y)
    assert appellf1(a, b1, b1, c, y, x) == appellf1(a, b1, b1, c, x, y)
    assert appellf1(a, b1, b2, c, S.Zero, S.Zero) is S.One

    f = appellf1(a, b1, b2, c, S.Zero, S.Zero, evaluate=False)
    assert f.func is appellf1
    assert f.doit() is S.One


def test_appellf1():
    mp.dps = 15
    assert appellf1(2,-2,1,1,2,3).ae(-1.75)
    assert appellf1(2,1,-2,1,2,3).ae(-8)
    assert appellf1(2,1,-2,1,0.5,0.25).ae(1.5)
    assert appellf1(-2,1,3,2,3,3).ae(19)
    assert appellf1(1,2,3,4,0.5,0.125).ae( 1.53843285792549786518)

