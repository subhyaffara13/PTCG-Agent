
def test_UGate():
    a, b, c, d = symbols('a,b,c,d')
    uMat = Matrix([[a, b], [c, d]])

    # Test basic case where gate exists in 1-qubit space
    u1 = UGate((0,), uMat)
    assert represent(u1, nqubits=1) == uMat
    assert qapply(u1*Qubit('0')) == a*Qubit('0') + c*Qubit('1')
    assert qapply(u1*Qubit('1')) == b*Qubit('0') + d*Qubit('1')

    # Test case where gate exists in a larger space
    u2 = UGate((1,), uMat)
    u2Rep = represent(u2, nqubits=2)
    for i in range(4):
        assert u2Rep*qubit_to_matrix(IntQubit(i, 2)) == \
            qubit_to_matrix(qapply(u2*IntQubit(i, 2)))

