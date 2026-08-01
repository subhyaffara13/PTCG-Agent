
def test_StateSpace_series():
    # For SISO Systems
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
    tf1 = TransferFunction(s, s+1, s)
    ser1 = Series(ss1, ss2)
    assert ser1 == Series(StateSpace(Matrix([
                            [0, 1],
                            [1, 0]]), Matrix([
                            [0],
                            [1]]), Matrix([[0, 1]]), Matrix([[0]])), StateSpace(Matrix([
                            [1, 0],
                            [0, 1]]), Matrix([
                            [1],
                            [0]]), Matrix([[1, 0]]), Matrix([[1]])))
    assert ser1.doit() == StateSpace(
                            Matrix([
                            [0, 1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 1, 1, 0],
                            [0, 0, 0, 1]]),
                            Matrix([
                            [0],
                            [1],
                            [0],
                            [0]]),
                            Matrix([[0, 1, 1, 0]]),
                            Matrix([[0]]))

    assert ser1.num_inputs == 1
    assert ser1.num_outputs == 1
    assert ser1.rewrite(TransferFunction) == TransferFunction(s**2, s**3 - s**2 - s + 1, s)
    ser2 = Series(ss1)
    ser3 = Series(ser2, ss2)
    assert ser3.doit() == ser1.doit()

    # TransferFunction interconnection with StateSpace
    ser_tf = Series(tf1, ss1)
    assert ser_tf == Series(TransferFunction(s, s + 1, s), StateSpace(Matrix([
                            [0, 1],
                            [1, 0]]), Matrix([
                            [0],
                            [1]]), Matrix([[0, 1]]), Matrix([[0]])))
    assert ser_tf.doit() == StateSpace(
                            Matrix([
                            [-1, 0,  0],
                            [0, 0,  1],
                            [-1, 1, 0]]),
                            Matrix([
                            [1],
                            [0],
                            [1]]),
                            Matrix([[0, 0, 1]]),
                            Matrix([[0]]))
    assert ser_tf.rewrite(TransferFunction) == TransferFunction(s**2, s**3 + s**2 - s - 1, s)

    # For MIMO Systems
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
    ser4 = MIMOSeries(ss3, ss4)
    assert ser4 == MIMOSeries(StateSpace(Matrix([
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
                    [ 0, 1]])))
    assert ser4.doit() == StateSpace(
                        Matrix([
                        [4,   1,  0, 0,  0],
                        [2,  -3,  0, 0,  0],
                        [2,   0,  -3, 4,  2],
                        [-6,  9, -1, -3,  0],
                        [-4, 9,  2, 5, 3]]),
                        Matrix([
                        [5,   2],
                        [-3,  -3],
                        [7,   -2],
                        [-12,  -3],
                        [-5, -5]]),
                        Matrix([
                        [-4, 12, 4, 2, -3],
                        [0, 1, 1, 4, 3]]),
                        Matrix([
                        [-2, -8],
                        [1, -1]]))
    assert ser4.num_inputs == ss3.num_inputs
    assert ser4.num_outputs == ss4.num_outputs
    ser5 = MIMOSeries(ss3)
    ser6 = MIMOSeries(ser5, ss4)
    assert ser6.doit() == ser4.doit()
    assert ser6.rewrite(TransferFunctionMatrix) == ser4.rewrite(TransferFunctionMatrix)
    tf2 = TransferFunction(1, s, s)
    tf3 = TransferFunction(1, s+1, s)
    tf4 = TransferFunction(s, s+2, s)
    tfm = TransferFunctionMatrix([[tf1, tf2], [tf3, tf4]])
    ser6 = MIMOSeries(ss3, tfm)
    assert ser6 == MIMOSeries(StateSpace(Matrix([
                        [4,  1],
                        [2, -3]]), Matrix([
                        [ 5,  2],
                        [-3, -3]]), Matrix([
                        [2, -4],
                        [0,  1]]), Matrix([
                        [3,  2],
                        [1, -1]])), TransferFunctionMatrix((
                        (TransferFunction(s, s + 1, s), TransferFunction(1, s, s)),
                        (TransferFunction(1, s + 1, s), TransferFunction(s, s + 2, s)))))

