
def test_matrix_to_qubits():
    qb = Qubit(0, 0, 0, 0)
    mat = Matrix([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    assert matrix_to_qubit(mat) == qb
    assert qubit_to_matrix(qb) == mat

    state = 2*sqrt(2)*(Qubit(0, 0, 0) + Qubit(0, 0, 1) + Qubit(0, 1, 0) +
                       Qubit(0, 1, 1) + Qubit(1, 0, 0) + Qubit(1, 0, 1) +
                       Qubit(1, 1, 0) + Qubit(1, 1, 1))
    ones = sqrt(2)*2*Matrix([1, 1, 1, 1, 1, 1, 1, 1])
    assert matrix_to_qubit(ones) == state.expand()
    assert qubit_to_matrix(state) == ones

