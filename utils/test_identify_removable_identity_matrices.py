
def test_identify_removable_identity_matrices():

    D = DiagonalMatrix(MatrixSymbol("D", k, k))

    cg = _array_contraction(_array_tensor_product(A, B, I), (1, 2, 4, 5))
    expected = _array_contraction(_array_tensor_product(A, B), (1, 2))
    assert identify_removable_identity_matrices(cg) == expected

    cg = _array_contraction(_array_tensor_product(A, B, C, I), (1, 3, 5, 6, 7))
    expected = _array_contraction(_array_tensor_product(A, B, C), (1, 3, 5))
    assert identify_removable_identity_matrices(cg) == expected

    # Tests with diagonal matrices:

    cg = _array_contraction(_array_tensor_product(A, B, D), (1, 2, 4, 5))
    ret = identify_removable_identity_matrices(cg)
    expected = _array_contraction(_array_tensor_product(A, B, D), (1, 4), (2, 5))
    assert ret == expected

    cg = _array_contraction(_array_tensor_product(A, B, D, M, N), (1, 2, 4, 5, 6, 8))
    ret = identify_removable_identity_matrices(cg)
    assert ret == cg

