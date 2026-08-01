
def test_transpose_multiplication(xp):
    _asarray = partial(xp.asarray, dtype=xp.complex128)
    class MyMatrix(interface.LinearOperator):
        def __init__(self, A):
            super().__init__(A.dtype, A.shape, xp=xp)
            self.A = A
        def _matmat(self, other): return self.A @ other
        def _rmatmat(self, other): return self.A.mT @ other

    A = MyMatrix(_asarray([[1, 2], [3, 4]]))
    X = _asarray([1, 2])
    X_T = X
    B = _asarray([[10, 20], [30, 40]])
    X2 = xp.reshape(X, (-1, 1))
    Y = _asarray([[1, 2], [3, 4]])

    xp_assert_equal(A @ B, Y @ B)
    xp_assert_equal(B.T @ A, B.T @ Y)
    xp_assert_equal(A.T @ B, Y.mT @ B)
    xp_assert_equal(A @ X, Y @ X)
    xp_assert_equal(X_T @ A, X_T @ Y)
    xp_assert_equal(A.T @ X, Y.mT @ X)
    xp_assert_equal(A @ X2, Y @ X2)
    xp_assert_equal(X2.mT @ A, X2.mT @ Y)
    xp_assert_equal(A.T @ X2, Y.mT @ X2)

