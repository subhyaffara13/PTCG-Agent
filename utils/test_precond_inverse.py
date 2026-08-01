
def test_precond_inverse(case, xp, batch_A, batch_b):
    if case.casename not in ('poisson1d', 'poisson2d'):
        pytest.skip("specific to poisson1d and poisson2d cases")
    if case.solver is qmr:
        pytest.skip("skipped for qmr")
    
    case = xp_case(case, xp, batch_A, batch_b, rng=38)
    rtol = 1e-8

    def inverse(b, which=None):
        """inverse preconditioner"""
        A = case.A
        if is_numpy(xp) and not isinstance(A, np.ndarray):
            A = A.toarray()
        return xp.linalg.solve(A, b[..., np.newaxis])

    def rinverse(b, which=None):
        """inverse preconditioner"""
        A = case.A
        if is_numpy(xp) and not isinstance(A, np.ndarray):
            A = A.toarray()
        return xp.linalg.solve(A.T, b[..., np.newaxis])

    matvec_count = [0]

    def matvec(b):
        matvec_count[0] += 1
        return case.A @ b[..., np.newaxis]

    def rmatvec(b):
        matvec_count[0] += 1
        return case.A.T @ b[..., np.newaxis]

    b = case.b
    x0 = 0 * b

    A = LinearOperator(case.A.shape, matvec, rmatvec=rmatvec)
    precond = LinearOperator(case.A.shape, inverse, rmatvec=rinverse)

    # Solve with preconditioner
    matvec_count = [0]
    x, info = case.solver(A, b, M=precond, x0=x0, rtol=rtol)

    assert info == 0
    _assert_success(A=case.A, x=x, b=b, xp=xp, rtol=rtol)

    # Solution should be nearly instant
    assert matvec_count[0] <= 3

