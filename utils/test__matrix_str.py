
def test_Matrix_str():
    M = Matrix([[x**+1, 1], [y, x + y]])
    assert str(M) == "Matrix([[x, 1], [y, x + y]])"
    assert sstr(M) == "Matrix([\n[x,     1],\n[y, x + y]])"
    M = Matrix([[1]])
    assert str(M) == sstr(M) == "Matrix([[1]])"
    M = Matrix([[1, 2]])
    assert str(M) == sstr(M) ==  "Matrix([[1, 2]])"
    M = Matrix()
    assert str(M) == sstr(M) == "Matrix(0, 0, [])"
    M = Matrix(0, 1, lambda i, j: 0)
    assert str(M) == sstr(M) == "Matrix(0, 1, [])"

