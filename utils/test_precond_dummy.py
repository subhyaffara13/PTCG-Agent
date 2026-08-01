
def test_precond_dummy(case, xp, batch_A, batch_b):
    dtype = case.A.dtype
    case = xp_case(case, xp, batch_A, batch_b)
    if (case.solver is cgs) and ("pd-F" in case.name):
        pytest.skip("Struggles to converge with single precision")
    if (case.solver is tfqmr) and ("poisson2d-F" in case.name):
        pytest.skip("Hits divide-by-zero with single precision")
    if not case.convergence:
        pytest.skip("Solver - Breakdown case, see gh-8829")

    rtol = 1e-8 if np.finfo(dtype).eps < 1e-8 else 1.2e-3

    A = case.A
    
    # NOTE: the following was previously uncommented as dead code --
    # was the intention to set `A = dia_array(...)`?

    # _, M, N = A.shape
    # # Ensure the diagonal elements of A are non-zero before calculating
    # # 1.0 / xp.linalg.diagonal(A)
    # diagOfA = xp.linalg.diagonal(A) if not is_numpy(xp) else A.diagonal()
    # if xp.count_nonzero(diagOfA) == diagOfA.shape[0]:
    #     dia_array(([1.0 / diagOfA], [0]), shape=(M, N))

    b = case.b
    x0 = 0 * b

    precond = IdentityOperator(shape=A.shape)

    if case.solver is qmr:
        x, info = case.solver(A, b, M1=precond, M2=precond, x0=x0, rtol=rtol)
    else:
        x, info = case.solver(A, b, M=precond, x0=x0, rtol=rtol)

    assert info == 0
    _assert_success(A=A, x=x, b=b, xp=np, rtol=rtol)

    A = aslinearoperator(A)

    x, info = case.solver(A, b, x0=x0, rtol=rtol)
    assert info == 0
    _assert_success(A=A, x=x, b=b, xp=np, rtol=rtol)

