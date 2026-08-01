
def test_swap_gate():
    """Test the SWAP gate."""
    swap_gate_matrix = Matrix(
        ((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
    assert represent(SwapGate(1, 0).decompose(), nqubits=2) == swap_gate_matrix
    assert qapply(SwapGate(1, 3)*Qubit('0010')) == Qubit('1000')
    nqubits = 4
    for i in range(nqubits):
        for j in range(i):
            assert represent(SwapGate(i, j), nqubits=nqubits) == \
                represent(SwapGate(i, j).decompose(), nqubits=nqubits)

