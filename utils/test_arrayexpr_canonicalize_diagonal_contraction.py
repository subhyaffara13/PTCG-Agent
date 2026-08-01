
def test_arrayexpr_canonicalize_diagonal_contraction():
    tp = _array_tensor_product(M, N, P, Q)
    expr = _array_contraction(_array_diagonal(tp, (1, 3, 4)), (0, 3))
    result = _array_diagonal(_array_contraction(_array_tensor_product(M, N, P, Q), (0, 6)), (0, 2, 3))
    assert expr == result

    expr = _array_contraction(_array_diagonal(tp, (0, 1, 2, 3, 7)), (1, 2, 3))
    result = _array_contraction(_array_tensor_product(M, N, P, Q), (0, 1, 2, 3, 5, 6, 7))
    assert expr == result

    expr = _array_contraction(_array_diagonal(tp, (0, 2, 6, 7)), (1, 2, 3))
    result = _array_diagonal(_array_contraction(tp, (3, 4, 5)), (0, 2, 3, 4))
    assert expr == result

    td = _array_diagonal(_array_tensor_product(M, N, P, Q), (0, 3))
    expr = _array_contraction(td, (2, 1), (0, 4, 6, 5, 3))
    result = _array_contraction(_array_tensor_product(M, N, P, Q), (0, 1, 3, 5, 6, 7), (2, 4))
    assert expr == result

