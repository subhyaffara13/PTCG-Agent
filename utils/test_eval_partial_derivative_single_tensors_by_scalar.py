
def test_eval_partial_derivative_single_tensors_by_scalar():

    tau, mu = symbols("tau mu")

    expr = PartialDerivative(tau**mu, tau)
    assert expr._perform_derivative() == mu*tau**mu/tau

    expr1a = PartialDerivative(A(i), tau)
    assert expr1a._perform_derivative() == 0

    expr1b = PartialDerivative(A(-i), tau)
    assert expr1b._perform_derivative() == 0

    expr2a = PartialDerivative(H(i, j), tau)
    assert expr2a._perform_derivative() == 0

    expr2b = PartialDerivative(H(i, -j), tau)
    assert expr2b._perform_derivative() == 0

    expr2c = PartialDerivative(H(-i, j), tau)
    assert expr2c._perform_derivative() == 0

    expr2d = PartialDerivative(H(-i, -j), tau)
    assert expr2d._perform_derivative() == 0

