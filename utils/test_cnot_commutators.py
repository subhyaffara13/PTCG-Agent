
def test_cnot_commutators():
    """Test commutators of involving CNOT gates."""
    assert Commutator(CNOT(0, 1), Z(0)).doit() == 0
    assert Commutator(CNOT(0, 1), T(0)).doit() == 0
    assert Commutator(CNOT(0, 1), S(0)).doit() == 0
    assert Commutator(CNOT(0, 1), X(1)).doit() == 0
    assert Commutator(CNOT(0, 1), CNOT(0, 1)).doit() == 0
    assert Commutator(CNOT(0, 1), CNOT(0, 2)).doit() == 0
    assert Commutator(CNOT(0, 2), CNOT(0, 1)).doit() == 0
    assert Commutator(CNOT(1, 2), CNOT(1, 0)).doit() == 0

