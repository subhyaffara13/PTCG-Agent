
def test_WGate():
    nqubits = 2
    basis_states = superposition_basis(nqubits)
    assert qapply(WGate(nqubits)*basis_states) == basis_states

    expected = ((2/sqrt(pow(2, nqubits)))*basis_states) - IntQubit(1, nqubits=nqubits)
    assert qapply(WGate(nqubits)*IntQubit(1, nqubits=nqubits)) == expected

