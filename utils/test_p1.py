
def test_P1():
    assert Matrix(3, 3, lambda i, j: j - i).diagonal(-1) == Matrix(
        1, 2, [-1, -1])

