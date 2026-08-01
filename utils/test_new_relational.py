
def test_new_relational():
    x = Symbol('x')

    assert Eq(x, 0) == Relational(x, 0)       # None ==> Equality
    assert Eq(x, 0) == Relational(x, 0, '==')
    assert Eq(x, 0) == Relational(x, 0, 'eq')
    assert Eq(x, 0) == Equality(x, 0)

    assert Eq(x, 0) != Relational(x, 1)       # None ==> Equality
    assert Eq(x, 0) != Relational(x, 1, '==')
    assert Eq(x, 0) != Relational(x, 1, 'eq')
    assert Eq(x, 0) != Equality(x, 1)

    assert Eq(x, -1) == Relational(x, -1)       # None ==> Equality
    assert Eq(x, -1) == Relational(x, -1, '==')
    assert Eq(x, -1) == Relational(x, -1, 'eq')
    assert Eq(x, -1) == Equality(x, -1)
    assert Eq(x, -1) != Relational(x, 1)       # None ==> Equality
    assert Eq(x, -1) != Relational(x, 1, '==')
    assert Eq(x, -1) != Relational(x, 1, 'eq')
    assert Eq(x, -1) != Equality(x, 1)

    assert Ne(x, 0) == Relational(x, 0, '!=')
    assert Ne(x, 0) == Relational(x, 0, '<>')
    assert Ne(x, 0) == Relational(x, 0, 'ne')
    assert Ne(x, 0) == Unequality(x, 0)
    assert Ne(x, 0) != Relational(x, 1, '!=')
    assert Ne(x, 0) != Relational(x, 1, '<>')
    assert Ne(x, 0) != Relational(x, 1, 'ne')
    assert Ne(x, 0) != Unequality(x, 1)

    assert Ge(x, 0) == Relational(x, 0, '>=')
    assert Ge(x, 0) == Relational(x, 0, 'ge')
    assert Ge(x, 0) == GreaterThan(x, 0)
    assert Ge(x, 1) != Relational(x, 0, '>=')
    assert Ge(x, 1) != Relational(x, 0, 'ge')
    assert Ge(x, 1) != GreaterThan(x, 0)
    assert (x >= 1) == Relational(x, 1, '>=')
    assert (x >= 1) == Relational(x, 1, 'ge')
    assert (x >= 1) == GreaterThan(x, 1)
    assert (x >= 0) != Relational(x, 1, '>=')
    assert (x >= 0) != Relational(x, 1, 'ge')
    assert (x >= 0) != GreaterThan(x, 1)

    assert Le(x, 0) == Relational(x, 0, '<=')
    assert Le(x, 0) == Relational(x, 0, 'le')
    assert Le(x, 0) == LessThan(x, 0)
    assert Le(x, 1) != Relational(x, 0, '<=')
    assert Le(x, 1) != Relational(x, 0, 'le')
    assert Le(x, 1) != LessThan(x, 0)
    assert (x <= 1) == Relational(x, 1, '<=')
    assert (x <= 1) == Relational(x, 1, 'le')
    assert (x <= 1) == LessThan(x, 1)
    assert (x <= 0) != Relational(x, 1, '<=')
    assert (x <= 0) != Relational(x, 1, 'le')
    assert (x <= 0) != LessThan(x, 1)

    assert Gt(x, 0) == Relational(x, 0, '>')
    assert Gt(x, 0) == Relational(x, 0, 'gt')
    assert Gt(x, 0) == StrictGreaterThan(x, 0)
    assert Gt(x, 1) != Relational(x, 0, '>')
    assert Gt(x, 1) != Relational(x, 0, 'gt')
    assert Gt(x, 1) != StrictGreaterThan(x, 0)
    assert (x > 1) == Relational(x, 1, '>')
    assert (x > 1) == Relational(x, 1, 'gt')
    assert (x > 1) == StrictGreaterThan(x, 1)
    assert (x > 0) != Relational(x, 1, '>')
    assert (x > 0) != Relational(x, 1, 'gt')
    assert (x > 0) != StrictGreaterThan(x, 1)

    assert Lt(x, 0) == Relational(x, 0, '<')
    assert Lt(x, 0) == Relational(x, 0, 'lt')
    assert Lt(x, 0) == StrictLessThan(x, 0)
    assert Lt(x, 1) != Relational(x, 0, '<')
    assert Lt(x, 1) != Relational(x, 0, 'lt')
    assert Lt(x, 1) != StrictLessThan(x, 0)
    assert (x < 1) == Relational(x, 1, '<')
    assert (x < 1) == Relational(x, 1, 'lt')
    assert (x < 1) == StrictLessThan(x, 1)
    assert (x < 0) != Relational(x, 1, '<')
    assert (x < 0) != Relational(x, 1, 'lt')
    assert (x < 0) != StrictLessThan(x, 1)

    # finally, some fuzz testing
    from sympy.core.random import randint
    for i in range(100):
        while 1:
            strtype, length = (chr, 65535) if randint(0, 1) else (chr, 255)
            relation_type = strtype(randint(0, length))
            if randint(0, 1):
                relation_type += strtype(randint(0, length))
            if relation_type not in ('==', 'eq', '!=', '<>', 'ne', '>=', 'ge',
                                     '<=', 'le', '>', 'gt', '<', 'lt', ':=',
                                     '+=', '-=', '*=', '/=', '%='):
                break

        raises(ValueError, lambda: Relational(x, 1, relation_type))
    assert all(Relational(x, 0, op).rel_op == '==' for op in ('eq', '=='))
    assert all(Relational(x, 0, op).rel_op == '!='
               for op in ('ne', '<>', '!='))
    assert all(Relational(x, 0, op).rel_op == '>' for op in ('gt', '>'))
    assert all(Relational(x, 0, op).rel_op == '<' for op in ('lt', '<'))
    assert all(Relational(x, 0, op).rel_op == '>=' for op in ('ge', '>='))
    assert all(Relational(x, 0, op).rel_op == '<=' for op in ('le', '<='))

