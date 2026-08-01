
def test_operator_represent():
    basis_kets = enumerate_states(operators_to_state(x_op), 1, 2)
    assert rep_expectation(
        x_op) == qapply(basis_kets[1].dual*x_op*basis_kets[0])

