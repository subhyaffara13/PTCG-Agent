
def test_ITE():
    assert lambdify((x, y, z), ITE(x, y, z))(True, 5, 3) == 5
    assert lambdify((x, y, z), ITE(x, y, z))(False, 5, 3) == 3


def test_ITE():
    ekpr = ITE(k < 1, m, n)
    assert rust_code(ekpr) == (
            "if (k < 1) {\n"
            "    m\n"
            "} else {\n"
            "    n\n"
            "}")


def test_ITE():
    A, B, C = symbols('A:C')
    assert ITE(True, False, True) is false
    assert ITE(True, True, False) is true
    assert ITE(False, True, False) is false
    assert ITE(False, False, True) is true
    assert isinstance(ITE(A, B, C), ITE)

    A = True
    assert ITE(A, B, C) == B
    A = False
    assert ITE(A, B, C) == C
    B = True
    assert ITE(And(A, B), B, C) == C
    assert ITE(Or(A, False), And(B, True), False) is false
    assert ITE(x, A, B) == Not(x)
    assert ITE(x, B, A) == x
    assert ITE(1, x, y) == x
    assert ITE(0, x, y) == y
    raises(TypeError, lambda: ITE(2, x, y))
    raises(TypeError, lambda: ITE(1, [], y))
    raises(TypeError, lambda: ITE(1, (), y))
    raises(TypeError, lambda: ITE(1, y, []))
    assert ITE(1, 1, 1) is S.true
    assert isinstance(ITE(1, 1, 1, evaluate=False), ITE)

    assert ITE(Eq(x, True), y, x) == ITE(x, y, x)
    assert ITE(Eq(x, False), y, x) == ITE(~x, y, x)
    assert ITE(Ne(x, True), y, x) == ITE(~x, y, x)
    assert ITE(Ne(x, False), y, x) == ITE(x, y, x)
    assert ITE(Eq(S.true, x), y, x) == ITE(x, y, x)
    assert ITE(Eq(S.false, x), y, x) == ITE(~x, y, x)
    assert ITE(Ne(S.true, x), y, x) == ITE(~x, y, x)
    assert ITE(Ne(S.false, x), y, x) == ITE(x, y, x)
    # 0 and 1 in the context are not treated as True/False
    # so the equality must always be False since dissimilar
    # objects cannot be equal
    assert ITE(Eq(x, 0), y, x) == x
    assert ITE(Eq(x, 1), y, x) == x
    assert ITE(Ne(x, 0), y, x) == y
    assert ITE(Ne(x, 1), y, x) == y
    assert ITE(Eq(x, 0), y, z).subs(x, 0) == y
    assert ITE(Eq(x, 0), y, z).subs(x, 1) == z
    raises(ValueError, lambda: ITE(x > 1, y, x, z))

