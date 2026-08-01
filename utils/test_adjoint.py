
def test_adjoint():
    dat = [[0, I], [1, 0]]
    ans = OperationsOnlyMatrix([[0, 1], [-I, 0]])
    assert ans.adjoint() == Matrix(dat)


def test_adjoint():
    dat = [[0, I], [1, 0]]
    ans = Matrix([[0, 1], [-I, 0]])
    for cls in classes:
        assert ans == cls(dat).adjoint()


def test_adjoint():
    dat = [[0, I], [1, 0]]
    ans = Matrix([[0, 1], [-I, 0]])
    for cls in all_classes:
        assert ans == cls(dat).adjoint()


def test_adjoint():
    Sq = MatrixSymbol('Sq', n, n)

    assert Adjoint(A).shape == (m, n)
    assert Adjoint(A*B).shape == (l, n)
    assert adjoint(Adjoint(A)) == A
    assert isinstance(Adjoint(Adjoint(A)), Adjoint)

    assert conjugate(Adjoint(A)) == Transpose(A)
    assert transpose(Adjoint(A)) == Adjoint(Transpose(A))

    assert Adjoint(eye(3)).doit() == eye(3)

    assert Adjoint(S(5)).doit() == S(5)

    assert Adjoint(Matrix([[1, 2], [3, 4]])).doit() == Matrix([[1, 3], [2, 4]])

    assert adjoint(trace(Sq)) == conjugate(trace(Sq))
    assert trace(adjoint(Sq)) == conjugate(trace(Sq))

    assert Adjoint(Sq)[0, 1] == conjugate(Sq[1, 0])

    assert Adjoint(A*B).doit() == Adjoint(B) * Adjoint(A)


def test_adjoint():
    assert adjoint(A*B) == Adjoint(B)*Adjoint(A)
    assert adjoint(2*A*B) == 2*Adjoint(B)*Adjoint(A)
    assert adjoint(2*I*C) == -2*I*Adjoint(C)

    M = Matrix(2, 2, [1, 2 + I, 3, 4])
    MA = Matrix(2, 2, [1, 3, 2 - I, 4])
    assert adjoint(M) == MA
    assert adjoint(2*M) == 2*MA
    assert adjoint(MatMul(2, M)) == MatMul(2, MA).doit()


def test_adjoint():
    a = Symbol('a', antihermitian=True)
    b = Symbol('b', hermitian=True)
    assert adjoint(a) == -a
    assert adjoint(I*a) == I*a
    assert adjoint(b) == b
    assert adjoint(I*b) == -I*b
    assert adjoint(a*b) == -b*a
    assert adjoint(I*a*b) == I*b*a

    x, y = symbols('x y')
    assert adjoint(adjoint(x)) == x
    assert adjoint(x + y) == conjugate(x) + conjugate(y)
    assert adjoint(x - y) == conjugate(x) - conjugate(y)
    assert adjoint(x * y) == conjugate(x) * conjugate(y)
    assert adjoint(x / y) == conjugate(x) / conjugate(y)
    assert adjoint(-x) == -conjugate(x)

    x, y = symbols('x y', commutative=False)
    assert adjoint(adjoint(x)) == x
    assert adjoint(x + y) == adjoint(x) + adjoint(y)
    assert adjoint(x - y) == adjoint(x) - adjoint(y)
    assert adjoint(x * y) == adjoint(y) * adjoint(x)
    assert adjoint(x / y) == 1 / adjoint(y) * adjoint(x)
    assert adjoint(-x) == -adjoint(x)


def test_adjoint():
    assert adjoint(A).is_commutative is False
    assert adjoint(A*A) == adjoint(A)**2
    assert adjoint(A*B) == adjoint(B)*adjoint(A)
    assert adjoint(A*B**2) == adjoint(B)**2*adjoint(A)
    assert adjoint(A*B - B*A) == adjoint(B)*adjoint(A) - adjoint(A)*adjoint(B)
    assert adjoint(A + I*B) == adjoint(A) - I*adjoint(B)

    assert adjoint(X) == X
    assert adjoint(-I*X) == I*X
    assert adjoint(Y) == -Y
    assert adjoint(-I*Y) == -I*Y

    assert adjoint(X) == conjugate(transpose(X))
    assert adjoint(Y) == conjugate(transpose(Y))
    assert adjoint(X) == transpose(conjugate(X))
    assert adjoint(Y) == transpose(conjugate(Y))

