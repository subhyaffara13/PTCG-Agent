
def test_as_dummy():
    _0, _1 = symbols('_0 _1')
    assert ConditionSet(x, x < 1, Interval(y, oo)
        ).as_dummy() == ConditionSet(_0, _0 < 1, Interval(y, oo))
    assert ConditionSet(x, x < 1, Interval(x, oo)
        ).as_dummy() == ConditionSet(_0, _0 < 1, Interval(x, oo))
    assert ConditionSet(x, x < 1, ImageSet(Lambda(y, y**2), S.Integers)
        ).as_dummy() == ConditionSet(
            _0, _0 < 1, ImageSet(Lambda(_0, _0**2), S.Integers))
    e = ConditionSet((x, y), x <= y, S.Reals**2)
    assert e.bound_symbols == [x, y]
    assert e.as_dummy() == ConditionSet((_0, _1), _0 <= _1, S.Reals**2)
    assert e.as_dummy() == ConditionSet((y, x), y <= x, S.Reals**2
        ).as_dummy()


def test_as_dummy():
    u, v, x, y, z, _0, _1 = symbols('u v x y z _0 _1')
    assert Lambda(x, x + 1).as_dummy() == Lambda(_0, _0 + 1)
    assert Lambda(x, x + _0).as_dummy() == Lambda(_1, _0 + _1)
    eq = (1 + Sum(x, (x, 1, x)))
    ans = 1 + Sum(_0, (_0, 1, x))
    once = eq.as_dummy()
    assert once == ans
    twice = once.as_dummy()
    assert twice == ans
    assert Integral(x + _0, (x, x + 1), (_0, 1, 2)
        ).as_dummy() == Integral(_0 + _1, (_0, x + 1), (_1, 1, 2))
    for T in (Symbol, Dummy):
        d = T('x', real=True)
        D = d.as_dummy()
        assert D != d and D.func == Dummy and D.is_real is None
    assert Dummy().as_dummy().is_commutative
    assert Dummy(commutative=False).as_dummy().is_commutative is False

