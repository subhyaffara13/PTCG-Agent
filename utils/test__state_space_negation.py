
def test_StateSpace_negation():
    A = Matrix([[a0, a1], [a2, a3]])
    B = Matrix([[b0, b1], [b2, b3]])
    C = Matrix([[c0, c1], [c1, c2], [c2, c3]])
    D = Matrix([[d0, d1], [d1, d2], [d2, d3]])
    SS = StateSpace(A, B, C, D)
    SS_neg = -SS

    state_mat = Matrix([[-1, 1], [1, -1]])
    input_mat = Matrix([1, -1])
    output_mat = Matrix([[-1, 1]])
    feedforward_mat = Matrix([1])
    system = StateSpace(state_mat, input_mat, output_mat, feedforward_mat)

    assert SS_neg == \
        StateSpace(Matrix([[a0, a1],
                           [a2, a3]]),
                   Matrix([[b0, b1],
                           [b2, b3]]),
                   Matrix([[-c0, -c1],
                           [-c1, -c2],
                           [-c2, -c3]]),
                   Matrix([[-d0, -d1],
                           [-d1, -d2],
                           [-d2, -d3]]))
    assert -system == \
        StateSpace(Matrix([[-1,  1],
                           [ 1, -1]]),
                   Matrix([[ 1],[-1]]),
                   Matrix([[1, -1]]),
                   Matrix([[-1]]))
    assert -SS_neg == SS
    assert -(-(-(-system))) == system

