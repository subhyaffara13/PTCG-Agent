
def test_arrayexpr_canonicalize_diagonal__permute_dims():
    tp = _array_tensor_product(M, Q, N, P)
    expr = _array_diagonal(
        _permute_dims(tp, [0, 1, 2, 4, 7, 6, 3, 5]), (2, 4, 5), (6, 7),
        (0, 3))
    result = _array_diagonal(tp, (2, 6, 7), (3, 5), (0, 4))
    assert expr == result

    tp = _array_tensor_product(M, N, P, Q)
    expr = _array_diagonal(_permute_dims(tp, [0, 5, 2, 4, 1, 6, 3, 7]), (1, 2, 6), (3, 4))
    result = _array_diagonal(_array_tensor_product(M, P, N, Q), (3, 4, 5), (1, 2))
    assert expr == result

