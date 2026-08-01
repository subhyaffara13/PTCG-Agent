
def test_convergence(case, xp, batch_A, batch_b):
    if (case.solver is tfqmr) and ("poisson2d-F" in case.name):
        pytest.skip("Struggles to converge with single precision on some platforms")
    case = xp_case(case, xp, batch_A, batch_b, rng=38)
    A = case.A

    if A.dtype in (xp.float64, xp.complex128):
        rtol = 1e-8
    else:
        rtol = 1e-2

    b = case.b
    x0 = 0 * b

    x, info = case.solver(A, b, x0=x0, rtol=rtol)
    xp_assert_equal(x0, 0 * b)  # ensure that x0 is not overwritten

    if case.convergence:
        assert info == 0
        _assert_success(A=A, x=x, b=b, xp=xp, rtol=rtol)
    else:
        assert info != 0
        _assert_success(A=A, x=x, b=b, xp=xp, rtol=1, less_equal=True)

