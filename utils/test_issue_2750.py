
def test_issue_2750():
    x = MatrixSymbol('x', 1, 1)
    assert (x.T*x).as_explicit()**-1 == Matrix([[x[0, 0]**(-2)]])

