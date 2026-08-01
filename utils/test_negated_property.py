
def test_negated_property():
    eq = Eq(x, y)
    assert eq.negated == Ne(x, y)

    eq = Ne(x, y)
    assert eq.negated == Eq(x, y)

    eq = Ge(x + y, y - x)
    assert eq.negated == Lt(x + y, y - x)

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(x, y).negated.negated == f(x, y)

