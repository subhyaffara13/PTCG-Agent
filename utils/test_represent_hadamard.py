
def test_represent_hadamard():
    """Test the representation of the hadamard gate."""
    circuit = HadamardGate(0)*Qubit('00')
    answer = represent(circuit, nqubits=2)
    # Check that the answers are same to within an epsilon.
    assert answer == Matrix([sqrt2_inv, sqrt2_inv, 0, 0])

