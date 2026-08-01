
def test_is_reducible():
    nqubits = 2
    (x, y, z, h) = create_gate_sequence()

    circuit = (x, y, y)
    assert is_reducible(circuit, nqubits, 1, 3) is True

    circuit = (x, y, x)
    assert is_reducible(circuit, nqubits, 1, 3) is False

    circuit = (x, y, y, x)
    assert is_reducible(circuit, nqubits, 0, 4) is True

    circuit = (x, y, y, x)
    assert is_reducible(circuit, nqubits, 1, 3) is True

    circuit = (x, y, z, y, y)
    assert is_reducible(circuit, nqubits, 1, 5) is True

