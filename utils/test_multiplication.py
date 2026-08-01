
def test_multiplication():
    w = omega
    assert w*(w + 1) == w*w + w
    assert (w + 1)*(w + 1) ==  w*w + w + 1
    assert w*1 == w
    assert 1*w == w
    assert w*ord0 == ord0
    assert ord0*w == ord0
    assert w**w == w * w**w
    assert (w**w)*w*w == w**(w + 2)


def test_multiplication():
    a = ArithmeticOnlyMatrix((
        (1, 2),
        (3, 1),
        (0, 6),
    ))

    b = ArithmeticOnlyMatrix((
        (1, 2),
        (3, 0),
    ))

    raises(ShapeError, lambda: b*a)
    raises(TypeError, lambda: a*{})

    c = a*b
    assert c[0, 0] == 7
    assert c[0, 1] == 2
    assert c[1, 0] == 6
    assert c[1, 1] == 6
    assert c[2, 0] == 18
    assert c[2, 1] == 0

    try:
        eval('c = a @ b')
    except SyntaxError:
        pass
    else:
        assert c[0, 0] == 7
        assert c[0, 1] == 2
        assert c[1, 0] == 6
        assert c[1, 1] == 6
        assert c[2, 0] == 18
        assert c[2, 1] == 0

    h = a.multiply_elementwise(c)
    assert h == matrix_multiply_elementwise(a, c)
    assert h[0, 0] == 7
    assert h[0, 1] == 4
    assert h[1, 0] == 18
    assert h[1, 1] == 6
    assert h[2, 0] == 0
    assert h[2, 1] == 0
    raises(ShapeError, lambda: a.multiply_elementwise(b))

    c = b * Symbol("x")
    assert isinstance(c, ArithmeticOnlyMatrix)
    assert c[0, 0] == x
    assert c[0, 1] == 2*x
    assert c[1, 0] == 3*x
    assert c[1, 1] == 0

    c2 = x * b
    assert c == c2

    c = 5 * b
    assert isinstance(c, ArithmeticOnlyMatrix)
    assert c[0, 0] == 5
    assert c[0, 1] == 2*5
    assert c[1, 0] == 3*5
    assert c[1, 1] == 0

    try:
        eval('c = 5 @ b')
    except SyntaxError:
        pass
    else:
        assert isinstance(c, ArithmeticOnlyMatrix)
        assert c[0, 0] == 5
        assert c[0, 1] == 2*5
        assert c[1, 0] == 3*5
        assert c[1, 1] == 0

    # https://github.com/sympy/sympy/issues/22353
    A = Matrix(ones(3, 1))
    _h = -Rational(1, 2)
    B = Matrix([_h, _h, _h])
    assert A.multiply_elementwise(B) == Matrix([
        [_h],
        [_h],
        [_h]])


def test_multiplication():
    a = Matrix((
        (1, 2),
        (3, 1),
        (0, 6),
    ))

    b = Matrix((
        (1, 2),
        (3, 0),
    ))

    c = a*b
    assert c[0, 0] == 7
    assert c[0, 1] == 2
    assert c[1, 0] == 6
    assert c[1, 1] == 6
    assert c[2, 0] == 18
    assert c[2, 1] == 0

    try:
        eval('c = a @ b')
    except SyntaxError:
        pass
    else:
        assert c[0, 0] == 7
        assert c[0, 1] == 2
        assert c[1, 0] == 6
        assert c[1, 1] == 6
        assert c[2, 0] == 18
        assert c[2, 1] == 0

    h = matrix_multiply_elementwise(a, c)
    assert h == a.multiply_elementwise(c)
    assert h[0, 0] == 7
    assert h[0, 1] == 4
    assert h[1, 0] == 18
    assert h[1, 1] == 6
    assert h[2, 0] == 0
    assert h[2, 1] == 0
    raises(ShapeError, lambda: matrix_multiply_elementwise(a, b))

    c = b * Symbol("x")
    assert isinstance(c, Matrix)
    assert c[0, 0] == x
    assert c[0, 1] == 2*x
    assert c[1, 0] == 3*x
    assert c[1, 1] == 0

    c2 = x * b
    assert c == c2

    c = 5 * b
    assert isinstance(c, Matrix)
    assert c[0, 0] == 5
    assert c[0, 1] == 2*5
    assert c[1, 0] == 3*5
    assert c[1, 1] == 0

    try:
        eval('c = 5 @ b')
    except SyntaxError:
        pass
    else:
        assert isinstance(c, Matrix)
        assert c[0, 0] == 5
        assert c[0, 1] == 2*5
        assert c[1, 0] == 3*5
        assert c[1, 1] == 0


def test_multiplication():
    a = Matrix((
        (1, 2),
        (3, 1),
        (0, 6),
    ))

    b = Matrix((
        (1, 2),
        (3, 0),
    ))

    raises(ShapeError, lambda: b*a)
    raises(TypeError, lambda: a*{})

    c = a*b
    assert c[0, 0] == 7
    assert c[0, 1] == 2
    assert c[1, 0] == 6
    assert c[1, 1] == 6
    assert c[2, 0] == 18
    assert c[2, 1] == 0

    c = a @ b
    assert c[0, 0] == 7
    assert c[0, 1] == 2
    assert c[1, 0] == 6
    assert c[1, 1] == 6
    assert c[2, 0] == 18
    assert c[2, 1] == 0

    h = matrix_multiply_elementwise(a, c)
    assert h == a.multiply_elementwise(c)
    assert h[0, 0] == 7
    assert h[0, 1] == 4
    assert h[1, 0] == 18
    assert h[1, 1] == 6
    assert h[2, 0] == 0
    assert h[2, 1] == 0
    raises(ShapeError, lambda: matrix_multiply_elementwise(a, b))

    c = b * Symbol("x")
    assert isinstance(c, Matrix)
    assert c[0, 0] == x
    assert c[0, 1] == 2*x
    assert c[1, 0] == 3*x
    assert c[1, 1] == 0

    c2 = x * b
    assert c == c2

    c = 5 * b
    assert isinstance(c, Matrix)
    assert c[0, 0] == 5
    assert c[0, 1] == 2*5
    assert c[1, 0] == 3*5
    assert c[1, 1] == 0

    M = Matrix([[oo, 0], [0, oo]])
    assert M ** 2 == M

    M = Matrix([[oo, oo], [0, 0]])
    assert M ** 2 == Matrix([[nan, nan], [nan, nan]])

    # https://github.com/sympy/sympy/issues/22353
    A = Matrix(ones(3, 1))
    _h = -Rational(1, 2)
    B = Matrix([_h, _h, _h])
    assert A.multiply_elementwise(B) == Matrix([
        [_h],
        [_h],
        [_h]])


def test_multiplication():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', m, l)
    C = MatrixSymbol('C', n, n)

    assert (2*A*B).shape == (n, l)
    assert (A*0*B) == ZeroMatrix(n, l)
    assert (2*A).shape == A.shape

    assert A * ZeroMatrix(m, m) * B == ZeroMatrix(n, l)

    assert C * Identity(n) * C.I == Identity(n)

    assert B/2 == S.Half*B
    raises(NotImplementedError, lambda: 2/B)

    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, n)
    assert Identity(n) * (A + B) == A + B

    assert A**2*A == A**3
    assert A**2*(A.I)**3 == A.I
    assert A**3*(A.I)**2 == A


def test_multiplication(xp):
    r1 = Rotation.from_quat(xp.asarray([0, 0, 0, 1]))
    r2 = Rotation.from_quat(xp.asarray([0, 0, 0, 1]))
    r3 = r1 * r2
    xp_assert_close(r3.as_quat(), xp.asarray([0.0, 0, 0, 1]))

    # Check that multiplication with other types fails
    with pytest.raises(TypeError, match="unsupported operand type"):
        r1 * 2
    # Check that __mul__ returns NotImplemented so that other types can implement
    # __rmul__. See https://github.com/scipy/scipy/issues/21541
    assert r1.__mul__(1) is NotImplemented

