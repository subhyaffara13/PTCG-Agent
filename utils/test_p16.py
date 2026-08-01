
def test_P16():
    M = Matrix([[2*sqrt(2), 8],
                [6*sqrt(6), 24*sqrt(3)]])
    assert M.rank() == 1

