
def test_regression_arpackng_1315():
    # Check that issue arpack-ng/#1315 is not present.
    # Adapted from arpack-ng/TESTS/bug_1315_single.c
    # If this fails, then the installed ARPACK library is faulty.

    for dtype in [np.float32, np.float64]:
        np.random.seed(1234)

        w0 = np.arange(1, 1000+1).astype(dtype)
        A = diags_array([w0], offsets=[0], shape=(1000, 1000))

        v0 = np.random.rand(1000).astype(dtype)
        w, v = eigs(A, k=9, ncv=2*9+1, which="LM", v0=v0)

        assert_allclose(np.sort(w), np.sort(w0[-9:]),
                        rtol=1e-4)

