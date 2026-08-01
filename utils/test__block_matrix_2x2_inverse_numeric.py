
def test_BlockMatrix_2x2_inverse_numeric():
    """Test 2x2 block matrix inversion numerically for all 4 formulas"""
    M = Matrix([[1, 2], [3, 4]])
    # rank deficient matrices that have full rank when two of them combined
    D1 = Matrix([[1, 2], [2, 4]])
    D2 = Matrix([[1, 3], [3, 9]])
    D3 = Matrix([[1, 4], [4, 16]])
    assert D1.rank() == D2.rank() == D3.rank() == 1
    assert (D1 + D2).rank() == (D2 + D3).rank() == (D3 + D1).rank() == 2

    # Only A is invertible
    K = BlockMatrix([[M, D1], [D2, D3]])
    assert block_collapse(K.inv()).as_explicit() == K.as_explicit().inv()
    # Only B is invertible
    K = BlockMatrix([[D1, M], [D2, D3]])
    assert block_collapse(K.inv()).as_explicit() == K.as_explicit().inv()
    # Only C is invertible
    K = BlockMatrix([[D1, D2], [M, D3]])
    assert block_collapse(K.inv()).as_explicit() == K.as_explicit().inv()
    # Only D is invertible
    K = BlockMatrix([[D1, D2], [D3, M]])
    assert block_collapse(K.inv()).as_explicit() == K.as_explicit().inv()

