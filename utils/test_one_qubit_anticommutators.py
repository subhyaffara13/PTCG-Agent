
def test_one_qubit_anticommutators():
    """Test single qubit gate anticommutation relations."""
    for g1 in (IdentityGate, X, Y, Z, H):
        for g2 in (IdentityGate, X, Y, Z, H):
            e = AntiCommutator(g1(0), g2(0))
            a = matrix_to_zero(represent(e, nqubits=1, format='sympy'))
            b = matrix_to_zero(represent(e.doit(), nqubits=1, format='sympy'))
            assert a == b
            e = AntiCommutator(g1(0), g2(1))
            a = matrix_to_zero(represent(e, nqubits=2, format='sympy'))
            b = matrix_to_zero(represent(e.doit(), nqubits=2, format='sympy'))
            assert a == b

