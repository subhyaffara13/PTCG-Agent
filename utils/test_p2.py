
def test_P2():
    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    M.row_del(1)
    M.col_del(2)
    assert M == Matrix([[1, 2],
                        [7, 8]])

