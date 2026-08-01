
def test_eigsh_for_k_greater():
    # Test eigsh() for k beyond limits.
    rng = np.random.RandomState(1234)
    A_sparse = diags_array([1.0, -2.0, 1.0], offsets=[-1, 0, 1], shape=(4, 4))
    A = generate_matrix(4, sparse=False, rng=rng)
    M_dense = generate_matrix_symmetric(4, pos_definite=True, rng=rng)
    M_sparse = generate_matrix_symmetric(
        4, pos_definite=True, sparse=True, rng=rng)
    M_linop = aslinearoperator(M_dense)
    eig_tuple1 = eigh(A, b=M_dense)
    eig_tuple2 = eigh(A, b=M_sparse)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)

        assert_equal(eigsh(A, M=M_dense, k=4), eig_tuple1)
        assert_equal(eigsh(A, M=M_dense, k=5), eig_tuple1)
        assert_equal(eigsh(A, M=M_sparse, k=5), eig_tuple2)

        # M as LinearOperator
        assert_raises(TypeError, eigsh, A, M=M_linop, k=4)

        # Test 'A' for different types
        assert_raises(TypeError, eigsh, aslinearoperator(A), k=4)
        assert_raises(TypeError, eigsh, A_sparse, M=M_dense, k=4)

