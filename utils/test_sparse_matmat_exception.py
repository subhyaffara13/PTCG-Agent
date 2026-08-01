
def test_sparse_matmat_exception():
    B = sparse.eye_array(2)
    # well defined matmat via `aslinearoperator`
    A = interface.aslinearoperator(sparse.eye_array(2))
    assert isinstance(A @ B, sparse.sparray)
    assert isinstance(B @ A, sparse.sparray)
    xp_assert_equal((A @ B).toarray(), np.eye(2))
    xp_assert_equal((B @ A).toarray(), np.eye(2))
    # ill-defined matmat via default fallback to matvec
    A = interface.LinearOperator((2, 2), matvec=lambda x: x)
    msg = "Try wrapping the matrix with `aslinearoperator` first."
    with assert_raises(TypeError, match=msg):
        A @ B
    with assert_raises(TypeError, match=msg):
        B @ A
    # after using `aslinearoperator`
    B = interface.aslinearoperator(B)
    assert isinstance(A @ B, interface.LinearOperator)
    assert isinstance(B @ A, interface.LinearOperator)
    xp_assert_equal((A @ B).matvec(np.ones(2)), np.ones(2))

