
def test_UGate_OneQubitGate_combo():
    v, w, f, g = symbols('v w f g')
    uMat1 = ImmutableMatrix([[v, w], [f, g]])
    cMat1 = Matrix([[v, w + 1, 0, 0], [f + 1, g, 0, 0], [0, 0, v, w + 1], [0, 0, f + 1, g]])
    u1 = X(0) + UGate(0, uMat1)
    assert represent(u1, nqubits=2) == cMat1

    uMat2 = ImmutableMatrix([[1/sqrt(2), 1/sqrt(2)], [I/sqrt(2), -I/sqrt(2)]])
    cMat2_1 = Matrix([[Rational(1, 2) + I/2, Rational(1, 2) - I/2],
                      [Rational(1, 2) - I/2, Rational(1, 2) + I/2]])
    cMat2_2 = Matrix([[1, 0], [0, I]])
    u2 = UGate(0, uMat2)
    assert represent(H(0)*u2, nqubits=1) == cMat2_1
    assert represent(u2*H(0), nqubits=1) == cMat2_2

