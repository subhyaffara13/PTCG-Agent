
def test_weak_strict():
    for func in (Eq, Ne):
        eq = func(x, 1)
        assert eq.strict == eq.weak == eq
    eq = Gt(x, 1)
    assert eq.weak == Ge(x, 1)
    assert eq.strict == eq
    eq = Lt(x, 1)
    assert eq.weak == Le(x, 1)
    assert eq.strict == eq
    eq = Ge(x, 1)
    assert eq.strict == Gt(x, 1)
    assert eq.weak == eq
    eq = Le(x, 1)
    assert eq.strict == Lt(x, 1)
    assert eq.weak == eq

