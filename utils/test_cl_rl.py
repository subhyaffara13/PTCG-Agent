
def test_CL_RL():
    assert SparseMatrix(((1, 2), (3, 4))).row_list() == \
        [(0, 0, 1), (0, 1, 2), (1, 0, 3), (1, 1, 4)]
    assert SparseMatrix(((1, 2), (3, 4))).col_list() == \
        [(0, 0, 1), (1, 0, 3), (0, 1, 2), (1, 1, 4)]

