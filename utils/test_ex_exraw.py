
def test_EX_EXRAW():
    assert EXRAW.zero is S.Zero
    assert EXRAW.one is S.One

    assert EX(1) == EX.Expression(1)
    assert EX(1).ex is S.One
    assert EXRAW(1) is S.One

    # EX has cancelling but EXRAW does not
    assert 2*EX((x + y*x)/x) == EX(2 + 2*y) != 2*((x + y*x)/x)
    assert 2*EXRAW((x + y*x)/x) == 2*((x + y*x)/x) != (1 + y)

    assert EXRAW.convert_from(EX(1), EX) is EXRAW.one
    assert EX.convert_from(EXRAW(1), EXRAW) == EX.one

    assert EXRAW.from_sympy(S.One) is S.One
    assert EXRAW.to_sympy(EXRAW.one) is S.One
    raises(CoercionFailed, lambda: EXRAW.from_sympy([]))

    assert EXRAW.get_field() == EXRAW

    assert EXRAW.unify(EX) == EXRAW
    assert EX.unify(EXRAW) == EXRAW

