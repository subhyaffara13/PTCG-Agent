
def test_transpose_inverse_commute():
    n = Symbol('n')
    I = Identity(n)
    Z = ZeroMatrix(n, n)
    A = BlockMatrix([[I, Z], [Z, I]])

    assert block_collapse(A.transpose().inverse()) == A
    assert block_collapse(A.inverse().transpose()) == A

    assert block_collapse(MatPow(A.transpose(), -2)) == MatPow(A, -2)
    assert block_collapse(MatPow(A, -2).transpose()) == MatPow(A, -2)

