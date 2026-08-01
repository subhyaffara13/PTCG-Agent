
def test_cnot_gate():
    """Test the CNOT gate."""
    circuit = CNotGate(1, 0)
    assert represent(circuit, nqubits=2) == \
        Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    circuit = circuit*Qubit('111')
    assert matrix_to_qubit(represent(circuit, nqubits=3)) == \
        qapply(circuit)

    circuit = CNotGate(1, 0)
    assert Dagger(circuit) == circuit
    assert Dagger(Dagger(circuit)) == circuit
    assert circuit*circuit == 1

