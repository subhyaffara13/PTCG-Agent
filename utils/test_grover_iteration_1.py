
def test_grover_iteration_1():
    numqubits = 2
    basis_states = superposition_basis(numqubits)
    v = OracleGate(numqubits, return_one_on_one)
    expected = IntQubit(1, nqubits=numqubits)
    assert qapply(grover_iteration(basis_states, v)) == expected

