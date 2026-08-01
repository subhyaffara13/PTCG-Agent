
def test_represent_phasegate():
    """Test the representation of the S gate."""
    circuit = PhaseGate(0)*Qubit('01')
    answer = represent(circuit, nqubits=2)
    assert Matrix([0, I, 0, 0]) == answer

