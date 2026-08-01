
def test_H33():
    A, B, C = symbols('A, B, C', commutative=False)
    assert (Commutator(A, Commutator(B, C))
        + Commutator(B, Commutator(C, A))
        + Commutator(C, Commutator(A, B))).doit().expand() == 0

