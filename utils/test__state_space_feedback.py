
def test_StateSpace_feedback():
    # For SISO
    a1 = Matrix([[0, 1], [1, 0]])
    b1 = Matrix([[0], [1]])
    c1 = Matrix([[0, 1]])
    d1 = Matrix([[0]])
    a2 = Matrix([[1, 0], [0, 1]])
    b2 = Matrix([[1], [0]])
    c2 = Matrix([[1, 0]])
    d2 = Matrix([[1]])
    ss1 = StateSpace(a1, b1, c1, d1)
    ss2 = StateSpace(a2, b2, c2, d2)
    fd1 = Feedback(ss1, ss2)

    # Negative feedback
    assert fd1 == Feedback(StateSpace(Matrix([[0, 1], [1, 0]]), Matrix([[0], [1]]), Matrix([[0, 1]]), Matrix([[0]])),
                          StateSpace(Matrix([[1, 0],[0, 1]]), Matrix([[1],[0]]), Matrix([[1, 0]]), Matrix([[1]])), -1)
    assert fd1.doit() == StateSpace(Matrix([
                            [0,  1,  0, 0],
                            [1, -1, -1, 0],
                            [0,  1,  1, 0],
                            [0,  0,  0, 1]]), Matrix([
                            [0],
                            [1],
                            [0],
                            [0]]), Matrix(
                            [[0, 1, 0, 0]]), Matrix(
                            [[0]]))
    assert fd1.rewrite(TransferFunction) == TransferFunction(s*(s - 1), s**3 - s + 1, s)

    # Positive Feedback
    fd2 = Feedback(ss1, ss2, 1)
    assert fd2.doit() == StateSpace(Matrix([
                            [0, 1, 0, 0],
                            [1, 1, 1, 0],
                            [0, 1, 1, 0],
                            [0, 0, 0, 1]]), Matrix([
                            [0],
                            [1],
                            [0],
                            [0]]), Matrix(
                            [[0, 1, 0, 0]]), Matrix(
                            [[0]]))
    assert fd2.rewrite(TransferFunction) == TransferFunction(s*(s - 1), s**3 - 2*s**2 - s + 1, s)

    # Connection with TransferFunction
    tf1 = TransferFunction(s, s+1, s)
    fd3 = Feedback(ss1, tf1)
    assert fd3 == Feedback(StateSpace(Matrix([
                            [0, 1],
                            [1, 0]]), Matrix([
                            [0],
                            [1]]), Matrix([[0, 1]]), Matrix([[0]])),
                            TransferFunction(s, s + 1, s), -1)
    assert fd3.doit() == StateSpace (Matrix([
                            [0,  1,  0],
                            [1, -1,  1],
                            [0,  1, -1]]), Matrix([
                            [0],
                            [1],
                            [0]]), Matrix(
                            [[0, 1, 0]]), Matrix(
                            [[0]]))

    # For MIMO
    a3 = Matrix([[4, 1], [2, -3]])
    b3 = Matrix([[5, 2], [-3, -3]])
    c3 = Matrix([[2, -4], [0, 1]])
    d3 = Matrix([[3, 2], [1, -1]])
    a4 = Matrix([[-3, 4, 2], [-1, -3, 0], [2, 5, 3]])
    b4 = Matrix([[1, 4], [-3, -3], [-2, 1]])
    c4 = Matrix([[4, 2, -3], [1, 4, 3]])
    d4 = Matrix([[-2, 4], [0, 1]])
    ss3 = StateSpace(a3, b3, c3, d3)
    ss4 = StateSpace(a4, b4, c4, d4)

    # Negative Feedback
    fd4 = MIMOFeedback(ss3, ss4)
    assert fd4 == MIMOFeedback(StateSpace(Matrix([
                            [4,  1],
                            [2, -3]]), Matrix([
                            [ 5,  2],
                            [-3, -3]]), Matrix([
                            [2, -4],
                            [0,  1]]), Matrix([
                            [3,  2],
                            [1, -1]])), StateSpace(Matrix([
                            [-3,  4, 2],
                            [-1, -3, 0],
                            [ 2,  5, 3]]), Matrix([
                            [ 1,  4],
                            [-3, -3],
                            [-2,  1]]), Matrix([
                            [4, 2, -3],
                            [1, 4,  3]]), Matrix([
                            [-2, 4],
                            [ 0, 1]])), -1)
    assert fd4.doit() == StateSpace(Matrix([
                            [Rational(3), Rational(-3, 4), Rational(-15, 4), Rational(-37, 2), Rational(-15)],
                            [Rational(7, 2), Rational(-39, 8), Rational(9, 8), Rational(39, 4), Rational(9)],
                            [Rational(3), Rational(-41, 4), Rational(-45, 4), Rational(-51, 2), Rational(-19)],
                            [Rational(-9, 2), Rational(129, 8), Rational(73, 8), Rational(171, 4), Rational(36)],
                            [Rational(-3, 2), Rational(47, 8), Rational(31, 8), Rational(85, 4), Rational(18)]]), Matrix([
                            [Rational(-1, 4), Rational(19, 4)],
                            [Rational(3, 8), Rational(-21, 8)],
                            [Rational(1, 4), Rational(29, 4)],
                            [Rational(3, 8), Rational(-93, 8)],
                            [Rational(5, 8), Rational(-35, 8)]]), Matrix([
                            [Rational(1), Rational(-15, 4), Rational(-7, 4), Rational(-21, 2), Rational(-9)],
                            [Rational(1, 2), Rational(-13, 8), Rational(-13, 8), Rational(-19, 4), Rational(-3)]]), Matrix([
                            [Rational(-1, 4), Rational(11, 4)],
                            [Rational(1, 8), Rational(9, 8)]]))

    # Positive Feedback
    fd5 = MIMOFeedback(ss3, ss4, 1)
    assert fd5.doit() == StateSpace(Matrix([
                            [Rational(4, 7), Rational(62, 7), Rational(1), Rational(-8), Rational(-69, 7)],
                            [Rational(32, 7), Rational(-135, 14), Rational(-3, 2), Rational(3), Rational(36, 7)],
                            [Rational(-10, 7), Rational(41, 7), Rational(-4), Rational(-12), Rational(-97, 7)],
                            [Rational(12, 7), Rational(-111, 14), Rational(-5, 2), Rational(18), Rational(171, 7)],
                            [Rational(2, 7), Rational(-29, 14), Rational(-1, 2), Rational(10), Rational(81, 7)]]), Matrix([
                            [Rational(6, 7), Rational(-17, 7)],
                            [Rational(-9, 14), Rational(15, 14)],
                            [Rational(6, 7), Rational(-31, 7)],
                            [Rational(-27, 14), Rational(87, 14)],
                            [Rational(-15, 14), Rational(25, 14)]]), Matrix([
                            [Rational(-2, 7), Rational(11, 7), Rational(1), Rational(-4), Rational(-39, 7)],
                            [Rational(-2, 7), Rational(15, 14), Rational(-1, 2), Rational(-3), Rational(-18, 7)]]), Matrix([
                            [Rational(4, 7), Rational(-9, 7)],
                            [Rational(1, 14), Rational(-11, 14)]]))

