
def test_adjoint_conjugate(xp):
    X = xp.asarray([[1j]], dtype=xp.complex128)
    A = interface.aslinearoperator(X)

    B = 1j * A
    Y = 1j * X

    v = xp.asarray([1], dtype=xp.complex128)

    xp_assert_equal(B.dot(v), xp.vecdot(Y, v))
    xp_assert_equal(B.H.dot(v), xp.vecdot(xp.conj(Y.T), v))
    xp_assert_equal(B.adjoint().dot(v), xp.vecdot(xp.conj(Y.T), v))

