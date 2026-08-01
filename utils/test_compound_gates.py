
def test_compound_gates():
    """Test a compound gate representation."""
    circuit = YGate(0)*ZGate(0)*XGate(0)*HadamardGate(0)*Qubit('00')
    answer = represent(circuit, nqubits=2)
    assert Matrix([I/sqrt(2), I/sqrt(2), 0, 0]) == answer

