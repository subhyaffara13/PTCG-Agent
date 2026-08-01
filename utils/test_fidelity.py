
def test_fidelity():
    #test with kets
    up = JzKet(S.Half, S.Half)
    down = JzKet(S.Half, Rational(-1, 2))
    updown = (S.One/sqrt(2))*up + (S.One/sqrt(2))*down

    #check with matrices
    up_dm = represent(up * Dagger(up))
    down_dm = represent(down * Dagger(down))
    updown_dm = represent(updown * Dagger(updown))

    assert abs(fidelity(up_dm, up_dm) - 1) < 1e-3
    assert fidelity(up_dm, down_dm) < 1e-3
    assert abs(fidelity(up_dm, updown_dm) - (S.One/sqrt(2))) < 1e-3
    assert abs(fidelity(updown_dm, down_dm) - (S.One/sqrt(2))) < 1e-3

    #check with density
    up_dm = Density([up, 1.0])
    down_dm = Density([down, 1.0])
    updown_dm = Density([updown, 1.0])

    assert abs(fidelity(up_dm, up_dm) - 1) < 1e-3
    assert abs(fidelity(up_dm, down_dm)) < 1e-3
    assert abs(fidelity(up_dm, updown_dm) - (S.One/sqrt(2))) < 1e-3
    assert abs(fidelity(updown_dm, down_dm) - (S.One/sqrt(2))) < 1e-3

    #check mixed states with density
    updown2 = sqrt(3)/2*up + S.Half*down
    d1 = Density([updown, 0.25], [updown2, 0.75])
    d2 = Density([updown, 0.75], [updown2, 0.25])
    assert abs(fidelity(d1, d2) - 0.991) < 1e-3
    assert abs(fidelity(d2, d1) - fidelity(d1, d2)) < 1e-3

    #using qubits/density(pure states)
    state1 = Qubit('0')
    state2 = Qubit('1')
    state3 = S.One/sqrt(2)*state1 + S.One/sqrt(2)*state2
    state4 = sqrt(Rational(2, 3))*state1 + S.One/sqrt(3)*state2

    state1_dm = Density([state1, 1])
    state2_dm = Density([state2, 1])
    state3_dm = Density([state3, 1])

    assert fidelity(state1_dm, state1_dm) == 1
    assert fidelity(state1_dm, state2_dm) == 0
    assert abs(fidelity(state1_dm, state3_dm) - 1/sqrt(2)) < 1e-3
    assert abs(fidelity(state3_dm, state2_dm) - 1/sqrt(2)) < 1e-3

    #using qubits/density(mixed states)
    d1 = Density([state3, 0.70], [state4, 0.30])
    d2 = Density([state3, 0.20], [state4, 0.80])
    assert abs(fidelity(d1, d1) - 1) < 1e-3
    assert abs(fidelity(d1, d2) - 0.996) < 1e-3
    assert abs(fidelity(d1, d2) - fidelity(d2, d1)) < 1e-3

    #TODO: test for invalid arguments
    # non-square matrix
    mat1 = [[0, 0],
            [0, 0],
            [0, 0]]

    mat2 = [[0, 0],
            [0, 0]]
    raises(ValueError, lambda: fidelity(mat1, mat2))

    # unequal dimensions
    mat1 = [[0, 0],
            [0, 0]]
    mat2 = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    raises(ValueError, lambda: fidelity(mat1, mat2))

    # unsupported data-type
    x, y = 1, 2  # random values that is not a matrix
    raises(ValueError, lambda: fidelity(x, y))

