
def test_arrayexpr_convert_array_contraction_tp_additions():
    a = ArrayAdd(
        _array_tensor_product(M, N),
        _array_tensor_product(N, M)
    )
    tp = _array_tensor_product(P, a, Q)
    expr = _array_contraction(tp, (3, 4))
    expected = _array_tensor_product(
        P,
        ArrayAdd(
            _array_contraction(_array_tensor_product(M, N), (1, 2)),
            _array_contraction(_array_tensor_product(N, M), (1, 2)),
        ),
        Q
    )
    assert expr == expected
    assert convert_array_to_matrix(expr) == _array_tensor_product(P, M * N + N * M, Q)

    expr = _array_contraction(tp, (1, 2), (3, 4), (5, 6))
    result = _array_contraction(
        _array_tensor_product(
            P,
            ArrayAdd(
                _array_contraction(_array_tensor_product(M, N), (1, 2)),
                _array_contraction(_array_tensor_product(N, M), (1, 2)),
            ),
            Q
        ), (1, 2), (3, 4))
    assert expr == result
    assert convert_array_to_matrix(expr) == P * (M * N + N * M) * Q

