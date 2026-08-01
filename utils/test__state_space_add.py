
def test_StateSpace_add():
    A1 = Matrix([[4, 1],[2, -3]])
    B1 = Matrix([[5, 2],[-3, -3]])
    C1 = Matrix([[2, -4],[0, 1]])
    D1 = Matrix([[3, 2],[1, -1]])
    ss1 = StateSpace(A1, B1, C1, D1)

    A2 = Matrix([[-3, 4, 2],[-1, -3, 0],[2, 5, 3]])
    B2 = Matrix([[1, 4],[-3, -3],[-2, 1]])
    C2 = Matrix([[4, 2, -3],[1, 4, 3]])
    D2 = Matrix([[-2, 4],[0, 1]])
    ss2 = StateSpace(A2, B2, C2, D2)
    ss3 = StateSpace()
    ss4 = StateSpace(Matrix([1]), Matrix([2]), Matrix([3]), Matrix([4]))

    expected_add = \
        StateSpace(
        Matrix([
        [4,  1,  0,  0, 0],
        [2, -3,  0,  0, 0],
        [0,  0, -3,  4, 2],
        [0,  0, -1, -3, 0],
        [0,  0,  2,  5, 3]]),
        Matrix([
        [ 5,  2],
        [-3, -3],
        [ 1,  4],
        [-3, -3],
        [-2,  1]]),
        Matrix([
        [2, -4, 4, 2, -3],
        [0,  1, 1, 4,  3]]),
        Matrix([
        [1, 6],
        [1, 0]]))

    expected_mul = \
        StateSpace(
        Matrix([
        [ -3,   4,  2, 0,  0],
        [ -1,  -3,  0, 0,  0],
        [  2,   5,  3, 0,  0],
        [ 22,  18, -9, 4,  1],
        [-15, -18,  0, 2, -3]]),
        Matrix([
        [  1,   4],
        [ -3,  -3],
        [ -2,   1],
        [-10,  22],
        [  6, -15]]),
        Matrix([
        [14, 14, -3, 2, -4],
        [ 3, -2, -6, 0,  1]]),
        Matrix([
        [-6, 14],
        [-2,  3]]))

    assert ss1 + ss2 == expected_add
    assert ss1*ss2 == expected_mul
    assert ss3 + 1/2 == StateSpace(Matrix([[0]]), Matrix([[0]]), Matrix([[0]]), Matrix([[0.5]]))
    assert ss4*1.5 == StateSpace(Matrix([[1]]), Matrix([[2]]), Matrix([[4.5]]), Matrix([[6.0]]))
    assert 1.5*ss4 == StateSpace(Matrix([[1]]), Matrix([[3.0]]), Matrix([[3]]), Matrix([[6.0]]))
    raises(ShapeError, lambda: ss1 + ss3)
    raises(ShapeError, lambda: ss2*ss4)

