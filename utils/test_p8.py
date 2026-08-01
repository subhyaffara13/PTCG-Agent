
def test_P8():
    M = Matrix([[1, -2*I],
                [-3*I, 4]])
    assert M.norm(ord=S.Infinity) == 7

