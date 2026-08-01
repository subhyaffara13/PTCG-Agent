
def test_one_qubit_commutators():
    """Test single qubit gate commutation relations."""
    for g1 in (IdentityGate, X, Y, Z, H, T, S):
        for g2 in (IdentityGate, X, Y, Z, H, T, S):
            e = Commutator(g1(0), g2(0))
            a = matrix_to_zero(represent(e, nqubits=1, format='sympy'))
            b = matrix_to_zero(represent(e.doit(), nqubits=1, format='sympy'))
            assert a == b

            e = Commutator(g1(0), g2(1))
            assert e.doit() == 0

