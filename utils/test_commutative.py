
def test_commutative():
    c1 = C('CAdd', (1,2,3))
    c2 = C('CAdd', (x,y))
    result = list(unify(c1, c2, {}))
    assert  {x: 1, y: C('CAdd', (2, 3))} in result
    assert ({x: 2, y: C('CAdd', (1, 3))} in result or
            {x: 2, y: C('CAdd', (3, 1))} in result)


def test_commutative():
    x, y = symbols('x y', commutative=False)
    assert dotprint(x + y) == dotprint(y + x)
    assert dotprint(x*y) != dotprint(y*x)


def test_commutative():
    det_a = Determinant(A)
    det_b = Determinant(B)
    assert det_a.is_commutative
    assert det_b.is_commutative
    assert det_a * det_b == det_b * det_a


def test_commutative():
    """Test for commutativity of And and Or"""
    A, B = map(Boolean, symbols('A,B'))

    assert A & B == B & A
    assert A | B == B | A


def test_commutative():
    """By default objects are Q.commutative that is why it returns True
    for both key=True and key=False"""
    assert ask(Q.commutative(x)) is True
    assert ask(Q.commutative(x), ~Q.commutative(x)) is False
    assert ask(Q.commutative(x), Q.complex(x)) is True
    assert ask(Q.commutative(x), Q.imaginary(x)) is True
    assert ask(Q.commutative(x), Q.real(x)) is True
    assert ask(Q.commutative(x), Q.positive(x)) is True
    assert ask(Q.commutative(x), ~Q.commutative(y)) is True

    assert ask(Q.commutative(2*x)) is True
    assert ask(Q.commutative(2*x), ~Q.commutative(x)) is False

    assert ask(Q.commutative(x + 1)) is True
    assert ask(Q.commutative(x + 1), ~Q.commutative(x)) is False

    assert ask(Q.commutative(x**2)) is True
    assert ask(Q.commutative(x**2), ~Q.commutative(x)) is False

    assert ask(Q.commutative(log(x))) is True

