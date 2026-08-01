
def test_represent_ygate():
    """Test the representation of the Y gate."""
    circuit = YGate(0)*Qubit('00')
    answer = represent(circuit, nqubits=2)
    assert answer[0] == 0 and answer[1] == I and \
        answer[2] == 0 and answer[3] == 0

