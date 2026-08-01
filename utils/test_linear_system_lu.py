
def test_linear_systemLU():
    n = Symbol('n')

    M = Matrix([[1, 2, 0, 1], [1, 3, 2*n, 1], [4, -1, n**2, 1]])

    assert solve_linear_system_LU(M, [x, y, z]) == {z: -3/(n**2 + 18*n),
                                                  x: 1 - 12*n/(n**2 + 18*n),
                                                  y: 6*n/(n**2 + 18*n)}

