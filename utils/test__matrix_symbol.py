
def test_MatrixSymbol():
    """ Test printing a MatrixSymbol to a aesara variable. """
    XX = aesara_code_(X)
    assert isinstance(XX, TensorVariable)
    assert XX.broadcastable == (False, False)


def test_MatrixSymbol():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, n)
    assert julia_code(A*B) == "A * B"
    assert julia_code(B*A) == "B * A"
    assert julia_code(2*A*B) == "2 * A * B"
    assert julia_code(B*2*A) == "2 * B * A"
    assert julia_code(A*(B + 3*Identity(n))) == "A * (3 * eye(n) + B)"
    assert julia_code(A**(x**2)) == "A ^ (x .^ 2)"
    assert julia_code(A**3) == "A ^ 3"
    assert julia_code(A**S.Half) == "A ^ (1 // 2)"


def test_MatrixSymbol():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, n)
    assert maple_code(A * B) == "A.B"
    assert maple_code(B * A) == "B.A"
    assert maple_code(2 * A * B) == "2*A.B"
    assert maple_code(B * 2 * A) == "2*B.A"

    assert maple_code(
        A * (B + 3 * Identity(n))) == "A.(3*Matrix(n, shape = identity) + B)"

    assert maple_code(A ** (x ** 2)) == "MatrixPower(A, x^2)"
    assert maple_code(A ** 3) == "MatrixPower(A, 3)"
    assert maple_code(A ** (S.Half)) == "MatrixPower(A, 1/2)"


def test_MatrixSymbol():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    B = MatrixSymbol('B', n, n)
    assert mcode(A*B) == "A*B"
    assert mcode(B*A) == "B*A"
    assert mcode(2*A*B) == "2*A*B"
    assert mcode(B*2*A) == "2*B*A"
    assert mcode(A*(B + 3*Identity(n))) == "A*(3*eye(n) + B)"
    assert mcode(A**(x**2)) == "A^(x.^2)"
    assert mcode(A**3) == "A^3"
    assert mcode(A**S.Half) == "A^(1/2)"


def test_MatrixSymbol():
    """ Test printing a MatrixSymbol to a theano variable. """
    XX = theano_code_(X)
    assert isinstance(XX, tt.TensorVariable)
    assert XX.broadcastable == (False, False)


def test_MatrixSymbol():
    n, m, t = symbols('n,m,t')
    X = MatrixSymbol('X', n, m)
    assert X.shape == (n, m)
    raises(TypeError, lambda: MatrixSymbol('X', n, m)(t))  # issue 5855
    assert X.doit() == X

