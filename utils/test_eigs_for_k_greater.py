
def test_eigs_for_k_greater():
    # Test eigs() for k beyond limits.
    rng = np.random.RandomState(1234)
    A_sparse = diags_array([1.0, -2.0, 1.0], offsets=[-1, 0, 1], shape=(4, 4))
    A = generate_matrix(4, sparse=False, rng=rng)
    M_dense = rng.random((4, 4))
    M_sparse = generate_matrix(4, sparse=True, rng=rng)
    M_linop = aslinearoperator(M_dense)
    eig_tuple1 = eig(A, b=M_dense)
    eig_tuple2 = eig(A, b=M_sparse)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)

        assert_equal(eigs(A, M=M_dense, k=3), eig_tuple1)
        assert_equal(eigs(A, M=M_dense, k=4), eig_tuple1)
        assert_equal(eigs(A, M=M_dense, k=5), eig_tuple1)
        assert_equal(eigs(A, M=M_sparse, k=5), eig_tuple2)

        # M as LinearOperator
        assert_raises(TypeError, eigs, A, M=M_linop, k=3)

        # Test 'A' for different types
        assert_raises(TypeError, eigs, aslinearoperator(A), k=3)
        assert_raises(TypeError, eigs, A_sparse, k=3)

