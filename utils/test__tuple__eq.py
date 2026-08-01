
def test_Tuple_Eq():
    assert Eq(Tuple(), Tuple()) is S.true
    assert Eq(Tuple(1), 1) is S.false
    assert Eq(Tuple(1, 2), Tuple(1)) is S.false
    assert Eq(Tuple(1), Tuple(1)) is S.true
    assert Eq(Tuple(1, 2), Tuple(1, 3)) is S.false
    assert Eq(Tuple(1, 2), Tuple(1, 2)) is S.true
    assert unchanged(Eq, Tuple(1, x), Tuple(1, 2))
    assert Eq(Tuple(1, x), Tuple(1, 2)).subs(x, 2) is S.true
    assert unchanged(Eq, Tuple(1, 2), x)
    f = Function('f')
    assert unchanged(Eq, Tuple(1), f(x))
    assert Eq(Tuple(1), f(x)).subs(x, 1).subs(f, Lambda(y, (y,))) is S.true

