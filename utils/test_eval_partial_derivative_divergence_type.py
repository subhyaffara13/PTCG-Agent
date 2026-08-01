
def test_eval_partial_derivative_divergence_type():
    expr1a = PartialDerivative(A(i), A(i))
    expr1b = PartialDerivative(A(i), A(k))
    expr1c = PartialDerivative(L.delta(-i, k) * A(i), A(k))

    assert (expr1a._perform_derivative()
            - (L.delta(-i, k) * expr1b._perform_derivative())).contract_delta(L.delta) == 0

    assert (expr1a._perform_derivative()
            - expr1c._perform_derivative()).contract_delta(L.delta) == 0

    expr2a = PartialDerivative(H(i, j), H(i, j))
    expr2b = PartialDerivative(H(i, j), H(k, m))
    expr2c = PartialDerivative(L.delta(-i, k) * L.delta(-j, m) * H(i, j), H(k, m))

    assert (expr2a._perform_derivative()
            - (L.delta(-i, k) * L.delta(-j, m) * expr2b._perform_derivative())).contract_delta(L.delta) == 0

    assert (expr2a._perform_derivative()
            - expr2c._perform_derivative()).contract_delta(L.delta) == 0

