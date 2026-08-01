
def test_P18():
    M = Matrix([[1,  0, -2, 0],
                [-2, 1,  0, 3],
                [-1, 2, -6, 6]])
    assert M.nullspace() == [Matrix([[2],
                                     [4],
                                     [1],
                                     [0]]),
                             Matrix([[0],
                                     [-3],
                                     [0],
                                     [1]])]

