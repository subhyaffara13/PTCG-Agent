
def test_hadamard_power_explicit():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    a, b = symbols('a b')

    assert HadamardPower(a, b) == a**b

    assert HadamardPower(a, B).as_explicit() == \
        Matrix([
            [a**B[0, 0], a**B[0, 1]],
            [a**B[1, 0], a**B[1, 1]]])

    assert HadamardPower(A, b).as_explicit() == \
        Matrix([
            [A[0, 0]**b, A[0, 1]**b],
            [A[1, 0]**b, A[1, 1]**b]])

    assert HadamardPower(A, B).as_explicit() == \
        Matrix([
            [A[0, 0]**B[0, 0], A[0, 1]**B[0, 1]],
            [A[1, 0]**B[1, 0], A[1, 1]**B[1, 1]]])

