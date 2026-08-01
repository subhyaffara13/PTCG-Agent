
def test_banded_lsoda():
    # expected solution is given by problem with full jacobian
    tfull, yfull = _solve_robertson_lsoda(use_jac=True, banded=False)

    for use_jac in [True, False]:
        t, y = _solve_robertson_lsoda(use_jac, True)
        assert_allclose(t, tfull)
        # Small tolerance to account for legitimate floating-point differences
        # After fixing tesco and banded Jacobian bugs, max relative error is ~1.5e-7
        assert_allclose(y, yfull, rtol=2e-7)

