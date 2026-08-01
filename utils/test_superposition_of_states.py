
def test_superposition_of_states():
    state = 1/sqrt(2)*Qubit('01') + 1/sqrt(2)*Qubit('10')
    state_gate = CNOT(0, 1)*HadamardGate(0)*state
    state_expanded = Qubit('01')/2 + Qubit('00')/2 - Qubit('11')/2 + Qubit('10')/2
    assert qapply(state_gate).expand() == state_expanded
    assert matrix_to_qubit(represent(state_gate, nqubits=2)) == state_expanded

