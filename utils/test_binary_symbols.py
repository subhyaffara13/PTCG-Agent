
def test_binary_symbols():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    assert Contains(x, FiniteSet(y, Eq(z, True))
        ).binary_symbols == {y, z}


def test_binary_symbols():
    assert ITE(x < 1, y, z).binary_symbols == {y, z}
    for f in (Eq, Ne):
        assert f(x, 1).binary_symbols == set()
        assert f(x, True).binary_symbols == {x}
        assert f(x, False).binary_symbols == {x}
    assert S.true.binary_symbols == set()
    assert S.false.binary_symbols == set()
    assert x.binary_symbols == {x}
    assert And(x, Eq(y, False), Eq(z, 1)).binary_symbols == {x, y}
    assert Q.prime(x).binary_symbols == set()
    assert Q.lt(x, 1).binary_symbols == set()
    assert Q.is_true(x).binary_symbols == {x}
    assert Q.eq(x, True).binary_symbols == {x}
    assert Q.prime(x).binary_symbols == set()


def test_binary_symbols():
    ans = {x}
    for f in Eq, Ne:
        for t in S.true, S.false:
            eq = f(x, S.true)
            assert eq.binary_symbols == ans
            assert eq.reversed.binary_symbols == ans
        assert f(x, 1).binary_symbols == set()

