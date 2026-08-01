
def test_zero_matrix_add():
    assert Add(ZeroMatrix(2, 2), ZeroMatrix(2, 2)) == ZeroMatrix(2, 2)

