
def test_rref_rhs():
    a, b, c, d = symbols('a b c d')
    A = Matrix([[0, 0], [0, 0], [1, 2], [3, 4]])
    B = Matrix([a, b, c, d])
    assert A.rref_rhs(B) == (Matrix([
    [1, 0],
    [0, 1],
    [0, 0],
    [0, 0]]), Matrix([
    [   -2*c + d],
    [3*c/2 - d/2],
    [          a],
    [          b]]))


def test_rref_rhs():
    a, b, c, d = symbols('a b c d')
    A = Matrix([[0, 0], [0, 0], [1, 2], [3, 4]])
    B = Matrix([a, b, c, d])
    assert A.rref_rhs(B) == (Matrix([
    [1, 0],
    [0, 1],
    [0, 0],
    [0, 0]]), Matrix([
    [   -2*c + d],
    [3*c/2 - d/2],
    [          a],
    [          b]]))

