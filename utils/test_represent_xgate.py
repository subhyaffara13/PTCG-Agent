
def test_represent_xgate():
    """Test the representation of the X gate."""
    circuit = XGate(0)*Qubit('00')
    answer = represent(circuit, nqubits=2)
    assert Matrix([0, 1, 0, 0]) == answer

