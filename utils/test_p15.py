
def test_P15():
    M = Matrix([[-1, 3,  7, -5],
                [4, -2,  1,  3],
                [2,  4, 15, -7]])
    assert M.rank() == 2

