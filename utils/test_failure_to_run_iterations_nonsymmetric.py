
def test_failure_to_run_iterations_nonsymmetric():
    """Check that the code exists gracefully without breaking
    if the matrix in not symmetric.
    """
    A = np.zeros((10, 10))
    A[0, 1] = 1
    Q = np.ones((10, 1))
    msg = "Exited at iteration 2|Exited postprocessing with accuracies.*"
    with pytest.warns(UserWarning, match=msg):
        eigenvalues, _ = lobpcg(A, Q, maxiter=20)
    assert np.max(eigenvalues) > 0

