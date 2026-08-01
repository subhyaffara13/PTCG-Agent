
def test_hadamard():
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 3, 3)
    v = MatrixSymbol('v', 3, 1)
    h = MatrixSymbol('h', 1, 3)
    C = HadamardProduct(A, B)
    assert maple_code(C) == "A*B"

    assert maple_code(C * v) == "(A*B).v"
    # HadamardProduct is higher than dot product.

    assert maple_code(h * C * v) == "h.(A*B).v"

    assert maple_code(C * A) == "(A*B).A"
    # mixing Hadamard and scalar strange b/c we vectorize scalars

    assert maple_code(C * x * y) == "x*y*(A*B)"


def test_hadamard():
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 3, 3)
    v = MatrixSymbol('v', 3, 1)
    h = MatrixSymbol('h', 1, 3)
    C = HadamardProduct(A, B)
    n = Symbol('n')
    assert mcode(C) == "A.*B"
    assert mcode(C*v) == "(A.*B)*v"
    assert mcode(h*C*v) == "h*(A.*B)*v"
    assert mcode(C*A) == "(A.*B)*A"
    # mixing Hadamard and scalar strange b/c we vectorize scalars
    assert mcode(C*x*y) == "(x.*y)*(A.*B)"

    # Testing HadamardPower:
    assert mcode(HadamardPower(A, n)) == "A.**n"
    assert mcode(HadamardPower(A, 1+n)) == "A.**(n + 1)"
    assert mcode(HadamardPower(A*B.T, 1+n)) == "(A*B.T).**(n + 1)"


def test_hadamard():
    m, n, p = symbols('m, n, p', integer=True)
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    X = MatrixSymbol('X', m, m)
    I = Identity(m)

    raises(TypeError, lambda: hadamard_product())
    assert hadamard_product(A) == A
    assert isinstance(hadamard_product(A, B), HadamardProduct)
    assert hadamard_product(A, B).doit() == hadamard_product(A, B)
    assert hadamard_product(X, I) == HadamardProduct(I, X)
    assert isinstance(hadamard_product(X, I), HadamardProduct)

    a = MatrixSymbol("a", k, 1)
    expr = MatAdd(ZeroMatrix(k, 1), OneMatrix(k, 1))
    expr = HadamardProduct(expr, a)
    assert expr.doit() == a

    raises(ValueError, lambda: HadamardProduct())

