
def test_maxit():
    """Check lobpcg if maxit=maxiter runs maxiter iterations and
    if maxit=None runs 20 iterations (the default)
    by checking the size of the iteration history output, which should
    be the number of iterations plus 3 (initial, final, and postprocessing)
    typically when maxiter is small and the choice of the best is passive.
    """
    rnd = np.random.RandomState(0)
    n = 50
    m = 4
    vals = -np.arange(1, n + 1)
    A = dia_array(([vals], [0]), shape=(n, n))
    A = A.astype(np.float32)
    X = rnd.standard_normal((n, m))
    X = X.astype(np.float64)
    msg = "Exited at iteration.*|Exited postprocessing with accuracies.*"
    for maxiter in range(1, 4):
        with pytest.warns(UserWarning, match=msg):
            _, _, l_h, r_h = lobpcg(A, X, tol=1e-8, maxiter=maxiter,
                                    retLambdaHistory=True,
                                    retResidualNormsHistory=True)
        assert_allclose(np.shape(l_h)[0], maxiter+3)
        assert_allclose(np.shape(r_h)[0], maxiter+3)
    with pytest.warns(UserWarning, match=msg):
        l, _, l_h, r_h = lobpcg(A, X, tol=1e-8,
                                retLambdaHistory=True,
                                retResidualNormsHistory=True)
    assert_allclose(np.shape(l_h)[0], 20+3)
    assert_allclose(np.shape(r_h)[0], 20+3)
    # Check that eigenvalue output is the last one in history
    assert_allclose(l, l_h[-1])
    # Make sure that both history outputs are lists
    assert isinstance(l_h, list)
    assert isinstance(r_h, list)
    # Make sure that both history lists are arrays-like
    assert_allclose(np.shape(l_h), np.shape(np.asarray(l_h)))
    assert_allclose(np.shape(r_h), np.shape(np.asarray(r_h)))

