
def test_arrayexpr_convert_array_to_matrix_diag2contraction_diagmatrix():
    cg = _array_diagonal(_array_tensor_product(M, a), (1, 2))
    res = _array_diag2contr_diagmatrix(cg)
    assert res.shape == cg.shape
    assert res == _array_contraction(_array_tensor_product(M, OneArray(1), DiagMatrix(a)), (1, 3))

    raises(ValueError, lambda: _array_diagonal(_array_tensor_product(a, M), (1, 2)))

    cg = _array_diagonal(_array_tensor_product(a.T, M), (1, 2))
    res = _array_diag2contr_diagmatrix(cg)
    assert res.shape == cg.shape
    assert res == _array_contraction(_array_tensor_product(OneArray(1), M, DiagMatrix(a.T)), (1, 4))

    cg = _array_diagonal(_array_tensor_product(a.T, M, N, b.T), (1, 2), (4, 7))
    res = _array_diag2contr_diagmatrix(cg)
    assert res.shape == cg.shape
    assert res == _array_contraction(
        _array_tensor_product(OneArray(1), M, N, OneArray(1), DiagMatrix(a.T), DiagMatrix(b.T)), (1, 7), (3, 9))

    cg = _array_diagonal(_array_tensor_product(a, M, N, b.T), (0, 2), (4, 7))
    res = _array_diag2contr_diagmatrix(cg)
    assert res.shape == cg.shape
    assert res == _array_contraction(
        _array_tensor_product(OneArray(1), M, N, OneArray(1), DiagMatrix(a), DiagMatrix(b.T)), (1, 6), (3, 9))

    cg = _array_diagonal(_array_tensor_product(a, M, N, b.T), (0, 4), (3, 7))
    res = _array_diag2contr_diagmatrix(cg)
    assert res.shape == cg.shape
    assert res == _array_contraction(
        _array_tensor_product(OneArray(1), M, N, OneArray(1), DiagMatrix(a), DiagMatrix(b.T)), (3, 6), (2, 9))

    I1 = Identity(1)
    x = MatrixSymbol("x", k, 1)
    A = MatrixSymbol("A", k, k)
    cg = _array_diagonal(_array_tensor_product(x, A.T, I1), (0, 2))
    assert _array_diag2contr_diagmatrix(cg).shape == cg.shape
    assert _array2matrix(cg).shape == cg.shape

