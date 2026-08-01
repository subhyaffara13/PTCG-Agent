
def test_random_circuit():
    c = random_circuit(10, 3)
    assert isinstance(c, Mul)
    m = represent(c, nqubits=3)
    assert m.shape == (8, 8)
    assert isinstance(m, Matrix)

