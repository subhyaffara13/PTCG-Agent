
def test_rel_subs():
    e = Relational(x, y, '==')
    e = e.subs(x, z)

    assert isinstance(e, Equality)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '>=')
    e = e.subs(x, z)

    assert isinstance(e, GreaterThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '<=')
    e = e.subs(x, z)

    assert isinstance(e, LessThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '>')
    e = e.subs(x, z)

    assert isinstance(e, StrictGreaterThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Relational(x, y, '<')
    e = e.subs(x, z)

    assert isinstance(e, StrictLessThan)
    assert e.lhs == z
    assert e.rhs == y

    e = Eq(x, 0)
    assert e.subs(x, 0) is S.true
    assert e.subs(x, 1) is S.false

