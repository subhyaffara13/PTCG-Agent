
def test_invariants():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', m, l)
    X = MatrixSymbol('X', n, n)
    objs = [Identity(n), ZeroMatrix(m, n), A, MatMul(A, B), MatAdd(A, A),
            Transpose(A), Adjoint(A), Inverse(X), MatPow(X, 2), MatPow(X, -1),
            MatPow(X, 0)]
    for obj in objs:
        assert obj == obj.__class__(*obj.args)

