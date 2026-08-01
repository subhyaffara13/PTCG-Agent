
def test_row_add():
    M = Matrix([[1,2,3],
               [4,5,6],
               [1,1,1]])
    M.row_add(2,0,5)
    assert M[0,0] == 6
    assert M[1,0] == 4
    assert M[0,2] == 8


def test_row_add():
    M = Matrix([[1,2,3],
               [4,5,6],
               [1,1,1]])
    M.row_add(2,0,5)
    assert M[0,0] == 6
    assert M[1,0] == 4
    assert M[0,2] == 8

