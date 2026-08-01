
def test_SparseMatrix():
    M = SparseMatrix([[x**+1, 1], [y, x + y]])
    assert str(M) == "Matrix([[x, 1], [y, x + y]])"
    assert sstr(M) == "Matrix([\n[x,     1],\n[y, x + y]])"

