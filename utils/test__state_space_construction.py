
def test_StateSpace_construction():
    # using different numbers for a SISO system.
    A1 = Matrix([[0, 1], [1, 0]])
    B1 = Matrix([1, 0])
    C1 = Matrix([[0, 1]])
    D1 = Matrix([0])
    ss1 = StateSpace(A1, B1, C1, D1)

    assert ss1.state_matrix == Matrix([[0, 1], [1, 0]])
    assert ss1.input_matrix == Matrix([1, 0])
    assert ss1.output_matrix == Matrix([[0, 1]])
    assert ss1.feedforward_matrix == Matrix([0])
    assert ss1.args == (Matrix([[0, 1], [1, 0]]), Matrix([[1], [0]]), Matrix([[0, 1]]), Matrix([[0]]))

    # using different symbols for a SISO system.
    ss2 = StateSpace(Matrix([a0]), Matrix([a1]),
                    Matrix([a2]), Matrix([a3]))

    assert ss2.state_matrix == Matrix([[a0]])
    assert ss2.input_matrix == Matrix([[a1]])
    assert ss2.output_matrix == Matrix([[a2]])
    assert ss2.feedforward_matrix == Matrix([[a3]])
    assert ss2.args == (Matrix([[a0]]), Matrix([[a1]]), Matrix([[a2]]), Matrix([[a3]]))

    # using different numbers for a MIMO system.
    ss3 = StateSpace(Matrix([[-1.5, -2], [1, 0]]),
                    Matrix([[0.5, 0], [0, 1]]),
                    Matrix([[0, 1], [0, 2]]),
                    Matrix([[2, 2], [1, 1]]))

    assert ss3.state_matrix == Matrix([[-1.5, -2], [1,  0]])
    assert ss3.input_matrix == Matrix([[0.5, 0], [0, 1]])
    assert ss3.output_matrix == Matrix([[0, 1], [0, 2]])
    assert ss3.feedforward_matrix == Matrix([[2, 2], [1, 1]])
    assert ss3.args == (Matrix([[-1.5, -2],
                                [1,  0]]),
                        Matrix([[0.5, 0],
                                [0, 1]]),
                        Matrix([[0, 1],
                                [0, 2]]),
                        Matrix([[2, 2],
                                [1, 1]]))

    # using different symbols for a MIMO system.
    A4 = Matrix([[a0, a1], [a2, a3]])
    B4 = Matrix([[b0, b1], [b2, b3]])
    C4 = Matrix([[c0, c1], [c2, c3]])
    D4 = Matrix([[d0, d1], [d2, d3]])
    ss4 = StateSpace(A4, B4, C4, D4)

    assert ss4.state_matrix == Matrix([[a0, a1], [a2, a3]])
    assert ss4.input_matrix == Matrix([[b0, b1], [b2, b3]])
    assert ss4.output_matrix == Matrix([[c0, c1], [c2, c3]])
    assert ss4.feedforward_matrix == Matrix([[d0, d1], [d2, d3]])
    assert ss4.args == (Matrix([[a0, a1],
                                [a2, a3]]),
                        Matrix([[b0, b1],
                                [b2, b3]]),
                        Matrix([[c0, c1],
                                [c2, c3]]),
                        Matrix([[d0, d1],
                                [d2, d3]]))

    # using less matrices. Rest will be filled with a minimum of zeros.
    ss5 = StateSpace()
    assert ss5.args == (Matrix([[0]]), Matrix([[0]]), Matrix([[0]]), Matrix([[0]]))

    A6 = Matrix([[0, 1], [1, 0]])
    B6 = Matrix([1, 1])
    ss6 = StateSpace(A6, B6)

    assert ss6.state_matrix == Matrix([[0, 1], [1, 0]])
    assert ss6.input_matrix ==  Matrix([1, 1])
    assert ss6.output_matrix == Matrix([[0, 0]])
    assert ss6.feedforward_matrix == Matrix([[0]])
    assert ss6.args == (Matrix([[0, 1],
                                [1, 0]]),
                        Matrix([[1],
                                [1]]),
                        Matrix([[0, 0]]),
                        Matrix([[0]]))

    # Check if the system is SISO or MIMO.
    # If system is not SISO, then it is definitely MIMO.

    assert ss1.is_SISO == True
    assert ss2.is_SISO == True
    assert ss3.is_SISO == False
    assert ss4.is_SISO == False
    assert ss5.is_SISO == True
    assert ss6.is_SISO == True

    # ShapeError if matrices do not fit.
    raises(ShapeError, lambda: StateSpace(Matrix([s, (s+1)**2]), Matrix([s+1]),
                                          Matrix([s**2 - 1]), Matrix([2*s])))
    raises(ShapeError, lambda: StateSpace(Matrix([s]), Matrix([s+1, s**3 + 1]),
                                          Matrix([s**2 - 1]), Matrix([2*s])))
    raises(ShapeError, lambda: StateSpace(Matrix([s]), Matrix([s+1]),
                                          Matrix([[s**2 - 1], [s**2 + 2*s + 1]]), Matrix([2*s])))
    raises(ShapeError, lambda: StateSpace(Matrix([[-s, -s], [s, 0]]),
                                                Matrix([[s/2, 0], [0, s]]),
                                                Matrix([[0, s]]),
                                                Matrix([[2*s, 2*s], [s, s]])))

    # TypeError if arguments are not sympy matrices.
    raises(TypeError, lambda: StateSpace(s**2, s+1, 2*s, 1))
    raises(TypeError, lambda: StateSpace(Matrix([2, 0.5]), Matrix([-1]),
                                         Matrix([1]), 0))

