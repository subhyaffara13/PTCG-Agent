
def test_reversedsign_property():
    eq = Eq(x, y)
    assert eq.reversedsign == Eq(-x, -y)

    eq = Ne(x, y)
    assert eq.reversedsign == Ne(-x, -y)

    eq = Ge(x + y, y - x)
    assert eq.reversedsign == Le(-x - y, x - y)

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(x, y).reversedsign.reversedsign == f(x, y)

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(-x, y).reversedsign.reversedsign == f(-x, y)

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(x, -y).reversedsign.reversedsign == f(x, -y)

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(-x, -y).reversedsign.reversedsign == f(-x, -y)

