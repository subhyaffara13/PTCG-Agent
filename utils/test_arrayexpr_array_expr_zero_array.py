
def test_arrayexpr_array_expr_zero_array():
    za1 = ZeroArray(k, l, m, n)
    zm1 = ZeroMatrix(m, n)

    za2 = ZeroArray(k, m, m, n)
    zm2 = ZeroMatrix(m, m)
    zm3 = ZeroMatrix(k, k)

    assert _array_tensor_product(M, N, za1) == ZeroArray(k, k, k, k, k, l, m, n)
    assert _array_tensor_product(M, N, zm1) == ZeroArray(k, k, k, k, m, n)

    assert _array_contraction(za1, (3,)) == ZeroArray(k, l, m)
    assert _array_contraction(zm1, (1,)) == ZeroArray(m)
    assert _array_contraction(za2, (1, 2)) == ZeroArray(k, n)
    assert _array_contraction(zm2, (0, 1)) == 0

    assert _array_diagonal(za2, (1, 2)) == ZeroArray(k, n, m)
    assert _array_diagonal(zm2, (0, 1)) == ZeroArray(m)

    assert _permute_dims(za1, [2, 1, 3, 0]) == ZeroArray(m, l, n, k)
    assert _permute_dims(zm1, [1, 0]) == ZeroArray(n, m)

    assert _array_add(za1) == za1
    assert _array_add(zm1) == ZeroArray(m, n)
    tp1 = _array_tensor_product(MatrixSymbol("A", k, l), MatrixSymbol("B", m, n))
    assert _array_add(tp1, za1) == tp1
    tp2 = _array_tensor_product(MatrixSymbol("C", k, l), MatrixSymbol("D", m, n))
    assert _array_add(tp1, za1, tp2) == _array_add(tp1, tp2)
    assert _array_add(M, zm3) == M
    assert _array_add(M, N, zm3) == _array_add(M, N)

