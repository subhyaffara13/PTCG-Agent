
def test_well_conditioned_problems():
    # Test that sparse the lsqr solver returns the right solution
    # on various problems with different random seeds.
    # This is a non-regression test for a potential ZeroDivisionError
    # raised when computing the `test2` & `test3` convergence conditions.
    n = 10
    A_sparse = scipy.sparse.eye_array(n, n)
    A_dense = A_sparse.toarray()

    with np.errstate(invalid='raise'):
        for seed in range(30):
            rng = np.random.RandomState(seed + 10)
            beta = rng.rand(n)
            beta[beta == 0] = 0.00001  # ensure that all the betas are not null
            b = A_sparse @ beta[:, np.newaxis]
            output = lsqr(A_sparse, b, show=show)

            # Check that the termination condition corresponds to an approximate
            # solution to Ax = b
            assert_equal(output[1], 1)
            solution = output[0]

            # Check that we recover the ground truth solution
            assert_allclose(solution, beta)

            # Sanity check: compare to the dense array solver
            reference_solution = np.linalg.solve(A_dense, b).ravel()
            assert_allclose(solution, reference_solution)

