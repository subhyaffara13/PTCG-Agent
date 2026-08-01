
def test_issue_7842():
    A = MatrixSymbol('A', 3, 1)
    B = MatrixSymbol('B', 2, 1)
    assert Eq(A, B) == False
    assert Eq(A[1,0], B[1, 0]).func is Eq
    A = ZeroMatrix(2, 3)
    B = ZeroMatrix(2, 3)
    assert Eq(A, B) == True

