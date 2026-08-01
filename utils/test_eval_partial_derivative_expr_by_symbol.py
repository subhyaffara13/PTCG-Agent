
def test_eval_partial_derivative_expr_by_symbol():

    tau, alpha = symbols("tau alpha")

    expr1 = PartialDerivative(tau**alpha, tau)
    assert expr1._perform_derivative() == alpha * 1 / tau * tau ** alpha

    expr2 = PartialDerivative(2*tau + 3*tau**4, tau)
    assert expr2._perform_derivative() == 2 + 12 * tau ** 3

    expr3 = PartialDerivative(2*tau + 3*tau**4, alpha)
    assert expr3._perform_derivative() == 0

