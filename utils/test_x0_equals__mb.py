
def test_x0_equals_Mb(case, xp, batch_A, batch_b):
    dtype = case.A.dtype
    case = xp_case(case, xp, batch_A, batch_b, rng=38)
    if (case.solver is cgs) and ("pd-F" in case.name):
        pytest.skip("Struggles to converge with single precision")
    if (case.solver is bicgstab) and (case.name == 'nonsymposdef-bicgstab'):
        pytest.skip("Solver fails due to numerical noise "
                    "on some architectures (see gh-15533).")
    if case.solver is tfqmr:
        pytest.skip("Solver does not support x0='Mb'")

    A = case.A
    b = case.b
    x0 = 'Mb'
    rtol = 1e-8 if np.finfo(dtype).eps < 1e-8 else 1.5e-3
    x, info = case.solver(A, b, x0=x0, rtol=rtol)

    assert x0 == 'Mb'  # ensure that x0 is not overwritten
    assert info == 0
    _assert_success(A=A, x=x, b=b, xp=xp, rtol=rtol)

