
def test_expm_multiply_dtype(dtype_a, dtype_b, b_is_matrix):
    """Make sure `expm_multiply` handles all numerical dtypes correctly."""
    assert_allclose_ = (partial(assert_allclose, rtol=1.8e-3, atol=1e-5)
                        if {dtype_a, dtype_b} & IMPRECISE else assert_allclose)
    rng = np.random.default_rng(1234)
    # test data
    n = 7
    b_shape = (n, 3) if b_is_matrix else (n, )
    if dtype_a in REAL_DTYPES:
        A = scipy.linalg.inv(rng.random([n, n])).astype(dtype_a)
    else:
        A = scipy.linalg.inv(
            rng.random([n, n]) + 1j*rng.random([n, n])
        ).astype(dtype_a)
    if dtype_b in REAL_DTYPES:
        B = (2*rng.random(b_shape)).astype(dtype_b)
    else:
        B = (rng.random(b_shape) + 1j*rng.random(b_shape)).astype(dtype_b)

    # single application
    sol_mat = expm_multiply(A, B)
    with estimated_warns():
        sol_op = expm_multiply(aslinearoperator(A), B)
    direct_sol = np.dot(sp_expm(A), B)
    assert_allclose_(sol_mat, direct_sol)
    assert_allclose_(sol_op, direct_sol)
    sol_op = expm_multiply(aslinearoperator(A), B, traceA=np.trace(A))
    assert_allclose_(sol_op, direct_sol)

    # for time points
    interval = {'start': 0.1, 'stop': 3.2, 'num': 13, 'endpoint': True}
    samples = np.linspace(**interval)
    X_mat = expm_multiply(A, B, **interval)
    with estimated_warns():
        X_op = expm_multiply(aslinearoperator(A), B, **interval)
    for sol_mat, sol_op, t in zip(X_mat, X_op, samples):
        direct_sol = sp_expm(t*A).dot(B)
        assert_allclose_(sol_mat, direct_sol)
        assert_allclose_(sol_op, direct_sol)

