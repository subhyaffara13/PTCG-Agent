
def test_linear_system():
    x, y, z, t, n = symbols('x, y, z, t, n')

    assert solve([x - 1, x - y, x - 2*y, y - 1], [x, y]) == []

    assert solve([x - 1, x - y, x - 2*y, x - 1], [x, y]) == []
    assert solve([x - 1, x - 1, x - y, x - 2*y], [x, y]) == []

    assert solve([x + 5*y - 2, -3*x + 6*y - 15], x, y) == {x: -3, y: 1}

    M = Matrix([[0, 0, n*(n + 1), (n + 1)**2, 0],
                [n + 1, n + 1, -2*n - 1, -(n + 1), 0],
                [-1, 0, 1, 0, 0]])

    assert solve_linear_system(M, x, y, z, t) == \
        {x: t*(-n-1)/n, y: 0, z: t*(-n-1)/n}

    assert solve([x + y + z + t, -z - t], x, y, z, t) == {x: -y, z: -t}

