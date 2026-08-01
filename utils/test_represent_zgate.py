
def test_represent_zgate():
    """Test the representation of the Z gate."""
    circuit = ZGate(0)*Qubit('00')
    answer = represent(circuit, nqubits=2)
    assert Matrix([1, 0, 0, 0]) == answer

