
def test_matrix_norm():
    # Vector Tests
    # Test columns and symbols
    x = Symbol('x', real=True)
    v = Matrix([cos(x), sin(x)])
    assert trigsimp(v.norm(2)) == 1
    assert v.norm(10) == Pow(cos(x)**10 + sin(x)**10, Rational(1, 10))

    # Test Rows
    A = Matrix([[5, Rational(3, 2)]])
    assert A.norm() == Pow(25 + Rational(9, 4), S.Half)
    assert A.norm(oo) == max(A)
    assert A.norm(-oo) == min(A)

    # Matrix Tests
    # Intuitive test
    A = Matrix([[1, 1], [1, 1]])
    assert A.norm(2) == 2
    assert A.norm(-2) == 0
    assert A.norm('frobenius') == 2
    assert eye(10).norm(2) == eye(10).norm(-2) == 1
    assert A.norm(oo) == 2

    # Test with Symbols and more complex entries
    A = Matrix([[3, y, y], [x, S.Half, -pi]])
    assert (A.norm('fro')
           == sqrt(Rational(37, 4) + 2*abs(y)**2 + pi**2 + x**2))

    # Check non-square
    A = Matrix([[1, 2, -3], [4, 5, Rational(13, 2)]])
    assert A.norm(2) == sqrt(Rational(389, 8) + sqrt(78665)/8)
    assert A.norm(-2) is S.Zero
    assert A.norm('frobenius') == sqrt(389)/2

    # Test properties of matrix norms
    # https://en.wikipedia.org/wiki/Matrix_norm#Definition
    # Two matrices
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 5], [-2, 2]])
    C = Matrix([[0, -I], [I, 0]])
    D = Matrix([[1, 0], [0, -1]])
    L = [A, B, C, D]
    alpha = Symbol('alpha', real=True)

    for order in ['fro', 2, -2]:
        # Zero Check
        assert zeros(3).norm(order) is S.Zero
        # Check Triangle Inequality for all Pairs of Matrices
        for X in L:
            for Y in L:
                dif = (X.norm(order) + Y.norm(order) -
                    (X + Y).norm(order))
                assert (dif >= 0)
        # Scalar multiplication linearity
        for M in [A, B, C, D]:
            dif = simplify((alpha*M).norm(order) -
                    abs(alpha) * M.norm(order))
            assert dif == 0

    # Test Properties of Vector Norms
    # https://en.wikipedia.org/wiki/Vector_norm
    # Two column vectors
    a = Matrix([1, 1 - 1*I, -3])
    b = Matrix([S.Half, 1*I, 1])
    c = Matrix([-1, -1, -1])
    d = Matrix([3, 2, I])
    e = Matrix([Integer(1e2), Rational(1, 1e2), 1])
    L = [a, b, c, d, e]
    alpha = Symbol('alpha', real=True)

    for order in [1, 2, -1, -2, S.Infinity, S.NegativeInfinity, pi]:
        # Zero Check
        if order > 0:
            assert Matrix([0, 0, 0]).norm(order) is S.Zero
        # Triangle inequality on all pairs
        if order >= 1:  # Triangle InEq holds only for these norms
            for X in L:
                for Y in L:
                    dif = (X.norm(order) + Y.norm(order) -
                        (X + Y).norm(order))
                    assert simplify(dif >= 0) is S.true
        # Linear to scalar multiplication
        if order in [1, 2, -1, -2, S.Infinity, S.NegativeInfinity]:
            for X in L:
                dif = simplify((alpha*X).norm(order) -
                    (abs(alpha) * X.norm(order)))
                assert dif == 0

    # ord=1
    M = Matrix(3, 3, [1, 3, 0, -2, -1, 0, 3, 9, 6])
    assert M.norm(1) == 13


def test_matrix_norm():
    # Vector Tests
    # Test columns and symbols
    x = Symbol('x', real=True)
    v = Matrix([cos(x), sin(x)])
    assert trigsimp(v.norm(2)) == 1
    assert v.norm(10) == Pow(cos(x)**10 + sin(x)**10, Rational(1, 10))

    # Test Rows
    A = Matrix([[5, Rational(3, 2)]])
    assert A.norm() == Pow(25 + Rational(9, 4), S.Half)
    assert A.norm(oo) == max(A)
    assert A.norm(-oo) == min(A)

    # Matrix Tests
    # Intuitive test
    A = Matrix([[1, 1], [1, 1]])
    assert A.norm(2) == 2
    assert A.norm(-2) == 0
    assert A.norm('frobenius') == 2
    assert eye(10).norm(2) == eye(10).norm(-2) == 1
    assert A.norm(oo) == 2

    # Test with Symbols and more complex entries
    A = Matrix([[3, y, y], [x, S.Half, -pi]])
    assert (A.norm('fro')
           == sqrt(Rational(37, 4) + 2*abs(y)**2 + pi**2 + x**2))

    # Check non-square
    A = Matrix([[1, 2, -3], [4, 5, Rational(13, 2)]])
    assert A.norm(2) == sqrt(Rational(389, 8) + sqrt(78665)/8)
    assert A.norm(-2) is S.Zero
    assert A.norm('frobenius') == sqrt(389)/2

    # Test properties of matrix norms
    # https://en.wikipedia.org/wiki/Matrix_norm#Definition
    # Two matrices
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 5], [-2, 2]])
    C = Matrix([[0, -I], [I, 0]])
    D = Matrix([[1, 0], [0, -1]])
    L = [A, B, C, D]
    alpha = Symbol('alpha', real=True)

    for order in ['fro', 2, -2]:
        # Zero Check
        assert zeros(3).norm(order) is S.Zero
        # Check Triangle Inequality for all Pairs of Matrices
        for X in L:
            for Y in L:
                dif = (X.norm(order) + Y.norm(order) -
                    (X + Y).norm(order))
                assert (dif >= 0)
        # Scalar multiplication linearity
        for M in [A, B, C, D]:
            dif = simplify((alpha*M).norm(order) -
                    abs(alpha) * M.norm(order))
            assert dif == 0

    # Test Properties of Vector Norms
    # https://en.wikipedia.org/wiki/Vector_norm
    # Two column vectors
    a = Matrix([1, 1 - 1*I, -3])
    b = Matrix([S.Half, 1*I, 1])
    c = Matrix([-1, -1, -1])
    d = Matrix([3, 2, I])
    e = Matrix([Integer(1e2), Rational(1, 1e2), 1])
    L = [a, b, c, d, e]
    alpha = Symbol('alpha', real=True)

    for order in [1, 2, -1, -2, S.Infinity, S.NegativeInfinity, pi]:
        # Zero Check
        if order > 0:
            assert Matrix([0, 0, 0]).norm(order) is S.Zero
        # Triangle inequality on all pairs
        if order >= 1:  # Triangle InEq holds only for these norms
            for X in L:
                for Y in L:
                    dif = (X.norm(order) + Y.norm(order) -
                        (X + Y).norm(order))
                    assert simplify(dif >= 0) is S.true
        # Linear to scalar multiplication
        if order in [1, 2, -1, -2, S.Infinity, S.NegativeInfinity]:
            for X in L:
                dif = simplify((alpha*X).norm(order) -
                    (abs(alpha) * X.norm(order)))
                assert dif == 0

    # ord=1
    M = Matrix(3, 3, [1, 3, 0, -2, -1, 0, 3, 9, 6])
    assert M.norm(1) == 13


def test_matrix_norm():
    x = np.arange(9).reshape((3, 3))
    actual = np.linalg.matrix_norm(x)

    assert_almost_equal(actual, np.float64(14.2828), double_decimal=3)

    actual = np.linalg.matrix_norm(x, keepdims=True)

    assert_almost_equal(actual, np.array([[14.2828]]), double_decimal=3)

