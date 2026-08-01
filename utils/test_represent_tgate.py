
def test_represent_tgate():
    """Test the representation of the T gate."""
    circuit = TGate(0)*Qubit('01')
    assert Matrix([0, exp(I*pi/4), 0, 0]) == represent(circuit, nqubits=2)

