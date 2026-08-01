
def test_integration_complex_sparse():
    # Regression test for gh-24671: solve_ivp with a complex ODE and
    # jac_sparsity should not emit ComplexWarning.
    rtol = 1e-3
    atol = 1e-6
    y0 = [0.5 + 1j]
    t_span = [0, 1]
    sparsity = csc_array(np.ones((1, 1)))
    res = solve_ivp(fun_complex, t_span, y0, method='BDF',
                    rtol=rtol, atol=atol, jac_sparsity=sparsity)
    assert res.success
    y_true = sol_complex(res.t)
    e = compute_error(res.y, y_true, rtol, atol)
    assert np.all(e < 5)

