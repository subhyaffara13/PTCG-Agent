
def test_StateSpace_parallel():
    # For SISO system
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
    p1 = Parallel(ss1, ss2)
    assert p1 == Parallel(StateSpace(Matrix([[0, 1], [1, 0]]), Matrix([[0], [1]]), Matrix([[0, 1]]), Matrix([[0]])),
                          StateSpace(Matrix([[1, 0],[0, 1]]), Matrix([[1],[0]]), Matrix([[1, 0]]), Matrix([[1]])))
    assert p1.doit() == StateSpace(Matrix([
                        [0, 1, 0, 0],
                        [1, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]),
                        Matrix([
                        [0],
                        [1],
                        [1],
                        [0]]),
                        Matrix([[0, 1, 1, 0]]),
                        Matrix([[1]]))
    assert p1.rewrite(TransferFunction) == TransferFunction(s*(s + 2), s**2 - 1, s)

    # Connecting StateSpace with TransferFunction
    tf1 = TransferFunction(s, s+1, s)
    p2 = Parallel(ss1, tf1)
    assert p2 == Parallel(StateSpace(Matrix([
                        [0, 1],
                        [1, 0]]), Matrix([
                        [0],
                        [1]]), Matrix([[0, 1]]), Matrix([[0]])), TransferFunction(s, s + 1, s))
    assert p2.doit() == StateSpace(
                        Matrix([
                        [0, 1,  0],
                        [1, 0,  0],
                        [0, 0, -1]]),
                        Matrix([
                        [0],
                        [1],
                        [1]]),
                        Matrix([[0, 1, -1]]),
                        Matrix([[1]]))
    assert p2.rewrite(TransferFunction) == TransferFunction(s**2, s**2 - 1, s)

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
    p3 = MIMOParallel(ss3, ss4)
    assert p3 == MIMOParallel(StateSpace(Matrix([
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
    assert p3.doit() == StateSpace(Matrix([
                        [4, 1, 0, 0, 0],
                        [2, -3, 0, 0, 0],
                        [0, 0, -3, 4, 2],
                        [0, 0, -1, -3, 0],
                        [0, 0, 2, 5, 3]]),
                        Matrix([
                        [5, 2],
                        [-3, -3],
                        [1, 4],
                        [-3, -3],
                        [-2, 1]]),
                        Matrix([
                        [2, -4, 4, 2, -3],
                        [0, 1, 1, 4, 3]]),
                        Matrix([
                        [1, 6],
                        [1, 0]]))

    # Using StateSpace with MIMOParallel.
    tf2 = TransferFunction(1, s, s)
    tf3 = TransferFunction(1, s + 1, s)
    tf4 = TransferFunction(s, s + 2, s)
    tfm = TransferFunctionMatrix([[tf1, tf2], [tf3, tf4]])
    p4 = MIMOParallel(tfm, ss3)
    assert p4 == MIMOParallel(TransferFunctionMatrix((
                        (TransferFunction(s, s + 1, s), TransferFunction(1, s, s)),
                        (TransferFunction(1, s + 1, s), TransferFunction(s, s + 2, s)))),
                        StateSpace(Matrix([
                        [4, 1],
                        [2, -3]]), Matrix([
                        [5, 2],
                        [-3, -3]]), Matrix([
                        [2, -4],
                        [0, 1]]), Matrix([
                        [3, 2],
                        [1, -1]])))

