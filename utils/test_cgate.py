
def test_cgate():
    """Test the general CGate."""
    # Test single control functionality
    CNOTMatrix = Matrix(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    assert represent(CGate(1, XGate(0)), nqubits=2) == CNOTMatrix

    # Test multiple control bit functionality
    ToffoliGate = CGate((1, 2), XGate(0))
    assert represent(ToffoliGate, nqubits=3) == \
        Matrix(
            [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0,
        1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0]])

    ToffoliGate = CGate((3, 0), XGate(1))
    assert qapply(ToffoliGate*Qubit('1001')) == \
        matrix_to_qubit(represent(ToffoliGate*Qubit('1001'), nqubits=4))
    assert qapply(ToffoliGate*Qubit('0000')) == \
        matrix_to_qubit(represent(ToffoliGate*Qubit('0000'), nqubits=4))

    CYGate = CGate(1, YGate(0))
    CYGate_matrix = Matrix(
        ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, -I), (0, 0, I, 0)))
    # Test 2 qubit controlled-Y gate decompose method.
    assert represent(CYGate.decompose(), nqubits=2) == CYGate_matrix

    CZGate = CGate(0, ZGate(1))
    CZGate_matrix = Matrix(
        ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, -1)))
    assert qapply(CZGate*Qubit('11')) == -Qubit('11')
    assert matrix_to_qubit(represent(CZGate*Qubit('11'), nqubits=2)) == \
        -Qubit('11')
    # Test 2 qubit controlled-Z gate decompose method.
    assert represent(CZGate.decompose(), nqubits=2) == CZGate_matrix

    CPhaseGate = CGate(0, PhaseGate(1))
    assert qapply(CPhaseGate*Qubit('11')) == \
        I*Qubit('11')
    assert matrix_to_qubit(represent(CPhaseGate*Qubit('11'), nqubits=2)) == \
        I*Qubit('11')

    # Test that the dagger, inverse, and power of CGate is evaluated properly
    assert Dagger(CZGate) == CZGate
    assert pow(CZGate, 1) == Dagger(CZGate)
    assert Dagger(CZGate) == CZGate.inverse()
    assert Dagger(CPhaseGate) != CPhaseGate
    assert Dagger(CPhaseGate) == CPhaseGate.inverse()
    assert Dagger(CPhaseGate) == pow(CPhaseGate, -1)
    assert pow(CPhaseGate, -1) == CPhaseGate.inverse()

