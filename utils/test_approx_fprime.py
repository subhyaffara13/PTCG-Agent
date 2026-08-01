
def test_approx_fprime():
    # check that approx_fprime (serviced by approx_derivative) works for
    # jac and hess
    g = optimize.approx_fprime(himmelblau_x0, himmelblau)
    assert_allclose(g, himmelblau_grad(himmelblau_x0), rtol=5e-6)

    h = optimize.approx_fprime(himmelblau_x0, himmelblau_grad)
    assert_allclose(h, himmelblau_hess(himmelblau_x0), rtol=5e-6)

