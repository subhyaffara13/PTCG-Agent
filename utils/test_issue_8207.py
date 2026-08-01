
def test_issue_8207():
    a = Matrix(MatrixSymbol('a', 3, 1))
    b = Matrix(MatrixSymbol('b', 3, 1))
    c = a.dot(b)
    d = diff(c, a[0, 0])
    e = diff(d, a[0, 0])
    assert d == b[0, 0]
    assert e == 0


def test_issue_8207():
    a = Matrix(MatrixSymbol('a', 3, 1))
    b = Matrix(MatrixSymbol('b', 3, 1))
    c = a.dot(b)
    d = diff(c, a[0, 0])
    e = diff(d, a[0, 0])
    assert d == b[0, 0]
    assert e == 0

