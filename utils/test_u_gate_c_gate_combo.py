
def test_UGate_CGate_combo():
    a, b, c, d = symbols('a,b,c,d')
    uMat = Matrix([[a, b], [c, d]])
    cMat = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, a, b], [0, 0, c, d]])

    # Test basic case where gate exists in 1-qubit space.
    u1 = UGate((0,), uMat)
    cu1 = CGate(1, u1)
    assert represent(cu1, nqubits=2) == cMat
    assert qapply(cu1*Qubit('10')) == a*Qubit('10') + c*Qubit('11')
    assert qapply(cu1*Qubit('11')) == b*Qubit('10') + d*Qubit('11')
    assert qapply(cu1*Qubit('01')) == Qubit('01')
    assert qapply(cu1*Qubit('00')) == Qubit('00')

    # Test case where gate exists in a larger space.
    u2 = UGate((1,), uMat)
    u2Rep = represent(u2, nqubits=2)
    for i in range(4):
        assert u2Rep*qubit_to_matrix(IntQubit(i, 2)) == \
            qubit_to_matrix(qapply(u2*IntQubit(i, 2)))

