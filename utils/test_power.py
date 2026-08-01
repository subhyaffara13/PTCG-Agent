
def test_power():
    c = FermionOp("c")
    assert c**0 == 1
    assert c**1 == c
    assert c**2 == 0
    assert c**3 == 0
    assert Dagger(c)**1 == Dagger(c)
    assert Dagger(c)**2 == 0

    assert (c**Symbol('a')).func == sympy.core.power.Pow
    assert (c**Symbol('a')).args == (c, Symbol('a'))

    with raises(ValueError):
        c**-1

    with raises(ValueError):
        c**3.2

    with raises(TypeError):
        c**1j


def test_power():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2))**2)

    A = ArithmeticOnlyMatrix([[2, 3], [4, 5]])
    assert (A**5)[:] == (6140, 8097, 10796, 14237)
    A = ArithmeticOnlyMatrix([[2, 1, 3], [4, 2, 4], [6, 12, 1]])
    assert (A**3)[:] == (290, 262, 251, 448, 440, 368, 702, 954, 433)
    assert A**0 == eye(3)
    assert A**1 == A
    assert (ArithmeticOnlyMatrix([[2]]) ** 100)[0, 0] == 2**100
    assert ArithmeticOnlyMatrix([[1, 2], [3, 4]])**Integer(2) == ArithmeticOnlyMatrix([[7, 10], [15, 22]])
    A = Matrix([[1,2],[4,5]])
    assert A.pow(20, method='cayley') == A.pow(20, method='multiply')


def test_power():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2))**2)

    R = Rational
    A = Matrix([[2, 3], [4, 5]])
    assert (A**-3)[:] == [R(-269)/8, R(153)/8, R(51)/2, R(-29)/2]
    assert (A**5)[:] == [6140, 8097, 10796, 14237]
    A = Matrix([[2, 1, 3], [4, 2, 4], [6, 12, 1]])
    assert (A**3)[:] == [290, 262, 251, 448, 440, 368, 702, 954, 433]
    assert A**0 == eye(3)
    assert A**1 == A
    assert (Matrix([[2]]) ** 100)[0, 0] == 2**100
    assert eye(2)**10000000 == eye(2)
    assert Matrix([[1, 2], [3, 4]])**Integer(2) == Matrix([[7, 10], [15, 22]])

    A = Matrix([[33, 24], [48, 57]])
    assert (A**S.Half)[:] == [5, 2, 4, 7]
    A = Matrix([[0, 4], [-1, 5]])
    assert (A**S.Half)**2 == A

    assert Matrix([[1, 0], [1, 1]])**S.Half == Matrix([[1, 0], [S.Half, 1]])
    assert Matrix([[1, 0], [1, 1]])**0.5 == Matrix([[1, 0], [0.5, 1]])
    from sympy.abc import n
    assert Matrix([[1, a], [0, 1]])**n == Matrix([[1, a*n], [0, 1]])
    assert Matrix([[b, a], [0, b]])**n == Matrix([[b**n, a*b**(n-1)*n], [0, b**n]])
    assert Matrix([
        [a**n, a**(n - 1)*n, (a**n*n**2 - a**n*n)/(2*a**2)],
        [   0,         a**n,                  a**(n - 1)*n],
        [   0,            0,                          a**n]])
    assert Matrix([[a, 1, 0], [0, a, 0], [0, 0, b]])**n == Matrix([
        [a**n, a**(n-1)*n, 0],
        [0, a**n, 0],
        [0, 0, b**n]])

    A = Matrix([[1, 0], [1, 7]])
    assert A._matrix_pow_by_jordan_blocks(S(3)) == A._eval_pow_by_recursion(3)
    A = Matrix([[2]])
    assert A**10 == Matrix([[2**10]]) == A._matrix_pow_by_jordan_blocks(S(10)) == \
        A._eval_pow_by_recursion(10)

    # testing a matrix that cannot be jordan blocked issue 11766
    m = Matrix([[3, 0, 0, 0, -3], [0, -3, -3, 0, 3], [0, 3, 0, 3, 0], [0, 0, 3, 0, 3], [3, 0, 0, 3, 0]])
    raises(MatrixError, lambda: m._matrix_pow_by_jordan_blocks(S(10)))

    # test issue 11964
    raises(MatrixError, lambda: Matrix([[1, 1], [3, 3]])._matrix_pow_by_jordan_blocks(S(-10)))
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])  # Nilpotent jordan block size 3
    assert A**10.0 == Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    raises(ValueError, lambda: A**2.1)
    raises(ValueError, lambda: A**Rational(3, 2))
    A = Matrix([[8, 1], [3, 2]])
    assert A**10.0 == Matrix([[1760744107, 272388050], [817164150, 126415807]])
    A = Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])  # Nilpotent jordan block size 1
    assert A**10.0 == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 1]])  # Nilpotent jordan block size 2
    assert A**10.0 == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    n = Symbol('n', integer=True)
    assert isinstance(A**n, MatPow)
    n = Symbol('n', integer=True, negative=True)
    raises(ValueError, lambda: A**n)
    n = Symbol('n', integer=True, nonnegative=True)
    assert A**n == Matrix([
        [KroneckerDelta(0, n), KroneckerDelta(1, n), -KroneckerDelta(0, n) - KroneckerDelta(1, n) + 1],
        [                   0, KroneckerDelta(0, n),                         1 - KroneckerDelta(0, n)],
        [                   0,                    0,                                                1]])
    assert A**(n + 2) == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    raises(ValueError, lambda: A**Rational(3, 2))
    A = Matrix([[0, 0, 1], [3, 0, 1], [4, 3, 1]])
    assert A**5.0 == Matrix([[168,  72,  89], [291, 144, 161], [572, 267, 329]])
    assert A**5.0 == A**5
    A = Matrix([[0, 1, 0],[-1, 0, 0],[0, 0, 0]])
    n = Symbol("n")
    An = A**n
    assert An.subs(n, 2).doit() == A**2
    raises(ValueError, lambda: An.subs(n, -2).doit())
    assert An * An == A**(2*n)

    # concretizing behavior for non-integer and complex powers
    A = Matrix([[0,0,0],[0,0,0],[0,0,0]])
    n = Symbol('n', integer=True, positive=True)
    assert A**n == A
    n = Symbol('n', integer=True, nonnegative=True)
    assert A**n == diag(0**n, 0**n, 0**n)
    assert (A**n).subs(n, 0) == eye(3)
    assert (A**n).subs(n, 1) == zeros(3)
    A = Matrix ([[2,0,0],[0,2,0],[0,0,2]])
    assert A**2.1 == diag (2**2.1, 2**2.1, 2**2.1)
    assert A**I == diag (2**I, 2**I, 2**I)
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 1]])
    raises(ValueError, lambda: A**2.1)
    raises(ValueError, lambda: A**I)
    A = Matrix([[S.Half, S.Half], [S.Half, S.Half]])
    assert A**S.Half == A
    A = Matrix([[1, 1],[3, 3]])
    assert A**S.Half == Matrix ([[S.Half, S.Half], [3*S.Half, 3*S.Half]])


def test_power():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2))**2)

    A = Matrix([[2, 3], [4, 5]])
    assert A**5 == Matrix([[6140, 8097], [10796, 14237]])
    A = Matrix([[2, 1, 3], [4, 2, 4], [6, 12, 1]])
    assert A**3 == Matrix([[290, 262, 251], [448, 440, 368], [702, 954, 433]])
    assert A**0 == eye(3)
    assert A**1 == A
    assert (Matrix([[2]]) ** 100)[0, 0] == 2**100
    assert Matrix([[1, 2], [3, 4]])**Integer(2) == Matrix([[7, 10], [15, 22]])
    A = Matrix([[1,2],[4,5]])
    assert A.pow(20, method='cayley') == A.pow(20, method='multiply')
    assert A**Integer(2) == Matrix([[9, 12], [24, 33]])
    assert eye(2)**10000000 == eye(2)

    A = Matrix([[33, 24], [48, 57]])
    assert (A**S.Half)[:] == [5, 2, 4, 7]
    A = Matrix([[0, 4], [-1, 5]])
    assert (A**S.Half)**2 == A

    assert Matrix([[1, 0], [1, 1]])**S.Half == Matrix([[1, 0], [S.Half, 1]])
    assert Matrix([[1, 0], [1, 1]])**0.5 == Matrix([[1, 0], [0.5, 1]])
    from sympy.abc import n
    assert Matrix([[1, a], [0, 1]])**n == Matrix([[1, a*n], [0, 1]])
    assert Matrix([[b, a], [0, b]])**n == Matrix([[b**n, a*b**(n-1)*n], [0, b**n]])
    assert Matrix([
        [a**n, a**(n - 1)*n, (a**n*n**2 - a**n*n)/(2*a**2)],
        [   0,         a**n,                  a**(n - 1)*n],
        [   0,            0,                          a**n]])
    assert Matrix([[a, 1, 0], [0, a, 0], [0, 0, b]])**n == Matrix([
        [a**n, a**(n-1)*n, 0],
        [0, a**n, 0],
        [0, 0, b**n]])

    A = Matrix([[1, 0], [1, 7]])
    assert A._matrix_pow_by_jordan_blocks(S(3)) == A._eval_pow_by_recursion(3)
    A = Matrix([[2]])
    assert A**10 == Matrix([[2**10]]) == A._matrix_pow_by_jordan_blocks(S(10)) == \
        A._eval_pow_by_recursion(10)

    # testing a matrix that cannot be jordan blocked issue 11766
    m = Matrix([[3, 0, 0, 0, -3], [0, -3, -3, 0, 3], [0, 3, 0, 3, 0], [0, 0, 3, 0, 3], [3, 0, 0, 3, 0]])
    raises(MatrixError, lambda: m._matrix_pow_by_jordan_blocks(S(10)))

    # test issue 11964
    raises(MatrixError, lambda: Matrix([[1, 1], [3, 3]])._matrix_pow_by_jordan_blocks(S(-10)))
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])  # Nilpotent jordan block size 3
    assert A**10.0 == Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    raises(ValueError, lambda: A**2.1)
    raises(ValueError, lambda: A**Rational(3, 2))
    A = Matrix([[8, 1], [3, 2]])
    assert A**10.0 == Matrix([[1760744107, 272388050], [817164150, 126415807]])
    A = Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])  # Nilpotent jordan block size 1
    assert A**10.0 == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 1]])  # Nilpotent jordan block size 2
    assert A**10.0 == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    n = Symbol('n', integer=True)
    assert isinstance(A**n, MatPow)
    n = Symbol('n', integer=True, negative=True)
    raises(ValueError, lambda: A**n)
    n = Symbol('n', integer=True, nonnegative=True)
    assert A**n == Matrix([
        [KroneckerDelta(0, n), KroneckerDelta(1, n), -KroneckerDelta(0, n) - KroneckerDelta(1, n) + 1],
        [                   0, KroneckerDelta(0, n),                         1 - KroneckerDelta(0, n)],
        [                   0,                    0,                                                1]])
    assert A**(n + 2) == Matrix([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
    raises(ValueError, lambda: A**Rational(3, 2))
    A = Matrix([[0, 0, 1], [3, 0, 1], [4, 3, 1]])
    assert A**5.0 == Matrix([[168,  72,  89], [291, 144, 161], [572, 267, 329]])
    assert A**5.0 == A**5
    A = Matrix([[0, 1, 0],[-1, 0, 0],[0, 0, 0]])
    n = Symbol("n")
    An = A**n
    assert An.subs(n, 2).doit() == A**2
    raises(ValueError, lambda: An.subs(n, -2).doit())
    assert An * An == A**(2*n)

    # concretizing behavior for non-integer and complex powers
    A = Matrix([[0,0,0],[0,0,0],[0,0,0]])
    n = Symbol('n', integer=True, positive=True)
    assert A**n == A
    n = Symbol('n', integer=True, nonnegative=True)
    assert A**n == diag(0**n, 0**n, 0**n)
    assert (A**n).subs(n, 0) == eye(3)
    assert (A**n).subs(n, 1) == zeros(3)
    A = Matrix ([[2,0,0],[0,2,0],[0,0,2]])
    assert A**2.1 == diag (2**2.1, 2**2.1, 2**2.1)
    assert A**I == diag (2**I, 2**I, 2**I)
    A = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 1]])
    raises(ValueError, lambda: A**2.1)
    raises(ValueError, lambda: A**I)
    A = Matrix([[S.Half, S.Half], [S.Half, S.Half]])
    assert A**S.Half == A
    A = Matrix([[1, 1],[3, 3]])
    assert A**S.Half == Matrix ([[S.Half, S.Half], [3*S.Half, 3*S.Half]])


def test_power():
    x, y, a, b, c = map(Symbol, 'xyabc')
    p, q, r = map(Wild, 'pqr')

    e = (x + y)**a
    assert e.match(p**q) == {p: x + y, q: a}
    assert e.match(p**p) is None

    e = (x + y)**(x + y)
    assert e.match(p**p) == {p: x + y}
    assert e.match(p**q) == {p: x + y, q: x + y}

    e = (2*x)**2
    assert e.match(p*q**r) == {p: 4, q: x, r: 2}

    e = Integer(1)
    assert e.match(x**p) == {p: 0}

