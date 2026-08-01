
def test_row_mult():
    M = Matrix([[1,2,3],
               [4,5,6]])
    M.row_mult(1,3)
    assert M[1,0] == 12
    assert M[0,0] == 1
    assert M[1,2] == 18


def test_row_mult():
    M = Matrix([[1,2,3],
               [4,5,6]])
    M.row_mult(1,3)
    assert M[1,0] == 12
    assert M[0,0] == 1
    assert M[1,2] == 18

