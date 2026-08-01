
def test_qft_represent():
    c = QFT(0, 3)
    a = represent(c, nqubits=3)
    b = represent(c.decompose(), nqubits=3)
    assert a.evalf(n=10) == b.evalf(n=10)

