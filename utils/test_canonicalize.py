
def test_canonicalize():
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    with warns_deprecated_sympy():
        expr = HadamardProduct(X, check=False)
    assert isinstance(expr, HadamardProduct)
    expr2 = expr.doit() # unpack is called
    assert isinstance(expr2, MatrixSymbol)
    Z = ZeroMatrix(2, 2)
    U = OneMatrix(2, 2)
    assert HadamardProduct(Z, X).doit() == Z
    assert HadamardProduct(U, X, X, U).doit() == HadamardPower(X, 2)
    assert HadamardProduct(X, U, Y).doit() == HadamardProduct(X, Y)
    assert HadamardProduct(X, Z, U, Y).doit() == Z

