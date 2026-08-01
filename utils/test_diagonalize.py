
def test_diagonalize():
    m = Matrix(2, 2, [0, -1, 1, 0])
    raises(MatrixError, lambda: m.diagonalize(reals_only=True))
    P, D = m.diagonalize()
    assert D.is_diagonal()
    assert D == Matrix([
                 [-I, 0],
                 [ 0, I]])

    # make sure we use floats out if floats are passed in
    m = Matrix(2, 2, [0, .5, .5, 0])
    P, D = m.diagonalize()
    assert all(isinstance(e, Float) for e in D.values())
    assert all(isinstance(e, Float) for e in P.values())

    _, D2 = m.diagonalize(reals_only=True)
    assert D == D2

    m = Matrix(
        [[0, 1, 0, 0], [1, 0, 0, 0.002], [0.002, 0, 0, 1], [0, 0, 1, 0]])
    P, D = m.diagonalize()
    assert allclose(P*D, m*P)

