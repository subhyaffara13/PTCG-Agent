
def test_matrixsymbol_solving():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    Z = ZeroMatrix(2, 2)
    assert -(-A + B) - A + B == Z
    assert (-(-A + B) - A + B).simplify() == Z
    assert (-(-A + B) - A + B).expand() == Z
    assert (-(-A + B) - A + B - Z).simplify() == Z
    assert (-(-A + B) - A + B - Z).expand() == Z
    assert (A*(A + B) + B*(A.T + B.T)).expand() == A**2 + A*B + B*A.T + B*B.T

