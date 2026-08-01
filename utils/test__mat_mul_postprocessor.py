
def test_MatMul_postprocessor():
    z = zeros(2)
    z1 = ZeroMatrix(2, 2)
    assert Mul(0, z) == Mul(z, 0) in [z, z1]

    M = Matrix([[1, 2], [3, 4]])
    Mx = Matrix([[x, 2*x], [3*x, 4*x]])
    assert Mul(x, M) == Mul(M, x) == Mx

    A = MatrixSymbol("A", 2, 2)
    assert Mul(A, M) == MatMul(A, M)
    assert Mul(M, A) == MatMul(M, A)
    # Scalars should be absorbed into constant matrices
    a = Mul(x, M, A)
    b = Mul(M, x, A)
    c = Mul(M, A, x)
    assert a == b == c == MatMul(Mx, A)
    a = Mul(x, A, M)
    b = Mul(A, x, M)
    c = Mul(A, M, x)
    assert a == b == c == MatMul(A, Mx)
    assert Mul(M, M) == M**2
    assert Mul(A, M, M) == MatMul(A, M**2)
    assert Mul(M, M, A) == MatMul(M**2, A)
    assert Mul(M, A, M) == MatMul(M, A, M)

    assert Mul(A, x, M, M, x) == MatMul(A, Mx**2)

