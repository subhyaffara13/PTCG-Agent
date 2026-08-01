
def test_transpose_noconjugate(xp):
    X = xp.asarray([[1j]], dtype=xp.complex128)
    A = interface.aslinearoperator(X)

    B = 1j * A
    Y = 1j * X

    v = xp.asarray([1], dtype=xp.complex128)

    xp_assert_equal(B.dot(v), xp.vecdot(Y, v))
    xp_assert_equal(B.T.dot(v), xp.vecdot(Y.T, v))

