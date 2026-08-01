
def test_eval_determinant(method, M, sol):
    assert method(M) == sol


def test_eval_determinant():
    assert det(Identity(n)) == 1
    assert det(ZeroMatrix(n, n)) == 0
    assert det(OneMatrix(n, n)) == Determinant(OneMatrix(n, n))
    assert det(OneMatrix(1, 1)) == 1
    assert det(OneMatrix(2, 2)) == 0
    assert det(Transpose(A)) == det(A)
    assert Determinant(MatMul(eye(2), eye(2))).doit(deep=True) == 1

