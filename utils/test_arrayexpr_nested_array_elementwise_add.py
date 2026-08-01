
def test_arrayexpr_nested_array_elementwise_add():
    cg = _array_contraction(_array_add(
        _array_tensor_product(M, N),
        _array_tensor_product(N, M)
    ), (1, 2))
    result = _array_add(
        _array_contraction(_array_tensor_product(M, N), (1, 2)),
        _array_contraction(_array_tensor_product(N, M), (1, 2))
    )
    assert cg == result

    cg = _array_diagonal(_array_add(
        _array_tensor_product(M, N),
        _array_tensor_product(N, M)
    ), (1, 2))
    result = _array_add(
        _array_diagonal(_array_tensor_product(M, N), (1, 2)),
        _array_diagonal(_array_tensor_product(N, M), (1, 2))
    )
    assert cg == result

