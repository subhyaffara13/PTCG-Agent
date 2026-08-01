
def test_atol(solver, xp, batch_A, batch_b):
    # TODO: minres / tfqmr. It didn't historically use absolute tolerances, so
    # fixing it is less urgent.
    if solver in (minres, tfqmr):
        pytest.skip("TODO: Add atol to minres/tfqmr")

    # Historically this is tested as below, all pass but for some reason
    # gcrotmk is over-sensitive to difference between random.seed/rng.random
    # Hence tol lower bound is changed from -10 to -9
    # np.random.seed(1234)
    # A = np.random.rand(10, 10)
    # A = A @ A.T + 10 * np.eye(10)
    # b = 1e3*np.random.rand(10)

    rng = np.random.default_rng(168441431005389)
    A = rng.uniform(size=(*batch_A, 10, 10))
    A = A @ A.mT + 10*np.eye(10)
    b = 1e3 * rng.uniform(size=(*batch_b, 10))

    dtype = xpx.default_dtype(xp)
    A = xp.asarray(A, dtype=dtype) 
    b = xp.asarray(b, dtype=dtype)

    tols = np.r_[0, np.logspace(-9, 2, 7), np.inf]

    # Check effect of badly scaled preconditioners
    M0 = rng.standard_normal(size=(*batch_A, 10, 10))
    M0 = xp.asarray(M0)
    M0 = M0 @ M0.mT
    Ms = [None, 1e-6 * M0, 1e6 * M0]

    for M, rtol, atol in itertools.product(Ms, tols, tols):
        if rtol == 0 and atol == 0:
            continue

        if solver is qmr:
            if M is not None:
                M = aslinearoperator(M)
                M2 = IdentityOperator(shape=(*batch_A, 10, 10))
            else:
                M2 = None
            x, info = solver(A, b, M1=M, M2=M2, rtol=rtol, atol=atol)
        else:
            x, info = solver(A, b, M=M, rtol=rtol, atol=atol)

        assert info == 0
        _assert_success(A=A, x=x, b=b, xp=xp, rtol=rtol, atol=atol)

