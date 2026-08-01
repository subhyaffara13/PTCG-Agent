
def test_batch(left, operator_definition, batch_A, batch_x, dtype, xp):
    # TODO ideas:
    # - test lower-precision types
    # - test `transpose`, `adjoint`, `__mul__`, etc.
    # - test composite LinearOperators
    rng = np.random.default_rng(41981392342349823)

    m, n, k = 4, 3, 2
    A_ = rng.random((*batch_A, m, n))
    x_row = rng.random((*batch_x, n if left else m))
    x_col = rng.random((*batch_x, n if left else m, 1))
    x_mat = rng.random((*batch_x, n if left else m, k))

    if dtype == np.complex128:
        A_ = A_ + 1j * rng.random(A_.shape)
        x_row = x_row + 1j * rng.random(x_row.shape)
        x_col = x_col + 1j * rng.random(x_col.shape)
        x_mat = x_mat + 1j * rng.random(x_mat.shape)
    
    A_, x_row, x_col, x_mat = (xp.asarray(x) for x in (A_, x_row, x_col, x_mat))

    def matvec(A, x):
        if not batch_x:
            assert x.ndim == 1
            return A @ x
        else:
            # It might make it easier on the author of LinearOperators to
            # "ravel" all batch dimensions into one before calling their `matvec`
            # implementation. That way, they only have to think about vectorizing
            # w.r.t. one batch dimension rather than an arbitrary number of batch
            # dimensions. In this case, `x.ndim` would be exactly 2.
            assert x.ndim >= 2
            return (A @ (x[..., xp.newaxis]))[..., 0]

    def matmat(A, X):
        if not batch_x:
            assert X.ndim == 2
        else:
            # Similar to above, we could ravel all batch dimensions before calling
            # the user's `matmat`. Then `x.ndim` would be exactly 3.
            assert X.ndim >= 3
        return A @ X

    if operator_definition == "aslinearoperator":
        A = interface.aslinearoperator(A_)
    elif operator_definition == "__init__matvec":
        A = interface.LinearOperator(
            shape=A_.shape, dtype=A_.dtype,
            matvec=lambda x: matvec(A_, x),
            rmatvec=lambda x: matvec(xp.conj(A_.mT), x),
            xp=xp,
        )
    elif operator_definition == "__init__matmat":
        # A = interface.LinearOperator(shape=A_.shape, dtype=A_.dtype,
        #                              matmat=lambda X: matmat(A_, X))
        pytest.skip("should work but doesn't - see gh-24510")
    elif operator_definition == "subclass_matvec":
        class MyLinearOperator(interface.LinearOperator):
            def _matvec(self, x):
                return matvec(A_, x)
            def _rmatvec(self, x):
                return matvec(xp.conj(A_.mT), x)
        A = MyLinearOperator(shape=A_.shape, dtype=A_.dtype, xp=xp)
    elif operator_definition == "subclass_matmat":
        class MyLinearOperator(interface.LinearOperator):
            def _matmat(self, X):
                return matmat(A_, X)
            def _rmatmat(self, X):
                return matmat(xp.conj(A_.mT), X)
        A = MyLinearOperator(shape=A_.shape, dtype=A_.dtype, xp=xp)

    # Test matvec
    # a. with row vector (or batch of row vectors)
    xp_assert_close(
        A.matvec(x_row) if left else A.rmatvec(x_row),
        matvec(A_, x_row) if left else matvec(xp.conj(A_.mT), x_row)
    )
    # b. with column vector (or batch of column vectors)
    if batch_x:
        message = "Dimension mismatch:..."
        with pytest.raises(ValueError, match=message):
            A.matvec(x_col) if left else A.rmatvec(x_col)
    else:
        message = ("Calling `matvec` on 'column vectors'..." if left
                   else "Calling `rmatvec` on 'column vectors'...")
        with pytest.warns(FutureWarning, match=message):
            xp_assert_close(
                A.matvec(x_col) if left else A.rmatvec(x_col),
                A_ @ x_col if left else xp.conj(A_.mT) @ x_col,
            )
    # c. with matrix (or batch of matrices)
    with pytest.raises(ValueError, match="Dimension mismatch:..."):
        A.matvec(x_mat) if left else A.rmatvec(x_mat)

    # Test matmat
    # a. with row vector (or batch of row vectors)
    message = "Dimension mismatch:..." if batch_x else "Expected at least 2-d..."
    with pytest.raises(ValueError, match=message):
        A.matmat(x_row) if left else A.rmatmat(x_row)
    # b. with column vector (or batch of column vectors)
    xp_assert_close(
        A.matmat(x_col) if left else A.rmatmat(x_col),
        A_ @ x_col if left else xp.conj(A_.mT) @ x_col,
    )
    # c. with matrix (or batch of matrices)
    xp_assert_close(
        A.matmat(x_mat) if left else A.rmatmat(x_mat),
        A_ @ x_mat if left else xp.conj(A_.mT) @ x_mat,
    )

    # test __matmul__ (via `@`), `__call__`, and `dot`
    if left:
        # a. with row vector (or batch of row vectors)
        if batch_x:
            with pytest.raises(ValueError, match="Dimension mismatch:..."):
                A @ x_row
        else:
            xp_assert_close(A @ x_row, A_ @ x_row)
            xp_assert_close(A(x_row), A_ @ x_row)
            xp_assert_close(A.dot(x_row), A_ @ x_row)
        # b. with column vector (or batch of column vectors)
        xp_assert_close(A @ x_col, A_ @ x_col)
        xp_assert_close(A(x_col), A_ @ x_col)
        xp_assert_close(A.dot(x_col), A_ @ x_col)
        # c. with matrix (or batch of matrices)
        xp_assert_close(A @ x_mat, A_ @ x_mat)
        xp_assert_close(A(x_mat), A_ @ x_mat)
        xp_assert_close(A.dot(x_mat), A_ @ x_mat)
    else:
        # a. with row vector (or batch of row vectors)
        broadcastable = True
        try:
            # `batch_x[-1]` becomes part of the core shape for matrix
            # multiplication with 1-D row vector
            # success thus depends on whether `batch_A` can broadcast
            # with `batch_x[:-1]`
            np.broadcast_shapes(batch_A, batch_x[:-1])
        except ValueError:
            broadcastable = False
        if not broadcastable:
            # Maybe should be "Dimension mismatch..."?
            msg = "Incompatible shapes|size of tensor|could not be broadcast..."
            with pytest.raises((ValueError, RuntimeError), match=msg):
                x_row @ A
        else:
            xp_assert_close(x_row @ A, x_row @ A_)
            xp_assert_close(A.rdot(x_row), x_row @ A_)
        # b. with column vector (or batch of column vectors)
        with pytest.raises(ValueError, match="Dimension mismatch:..."):
            x_col @ A
        # c. with matrix (or batch of matrices)
        xp_assert_close(xp.conj(x_mat.mT) @ A, xp.conj(x_mat.mT) @ A_)
        xp_assert_close(A.rdot(xp.conj(x_mat.mT)), xp.conj(x_mat.mT) @ A_)


def test_batch(f, args):
    rng = np.random.default_rng(283592436523456)
    batch_shape = (2, 3)
    m = 10
    A = rng.random(batch_shape + (m,))

    if f in {hankel}:
        message = "Beginning in SciPy 1.19, multidimensional input will be..."
        with pytest.warns(FutureWarning, match=message):
            f(A, *args)
        return

    res = f(A, *args)
    ref = np.asarray([f(a, *args) for a in A.reshape(-1, m)])
    ref = ref.reshape(A.shape[:-1] + ref.shape[-2:])
    assert_allclose(res, ref)

