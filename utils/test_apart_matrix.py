
def test_apart_matrix():
    M = Matrix(2, 2, lambda i, j: 1/(x + i + 1)/(x + j))

    assert apart(M) == Matrix([
        [1/x - 1/(x + 1), (x + 1)**(-2)],
        [1/(2*x) - (S.Half)/(x + 2), 1/(x + 1) - 1/(x + 2)],
    ])

