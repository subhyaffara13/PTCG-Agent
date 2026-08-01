
def test_array_contraction_to_diagonal_multiple_identities():

    expr = _array_contraction(_array_tensor_product(A, B, I, C), (1, 2, 4), (5, 6))
    assert _array_contraction_to_diagonal_multiple_identity(expr) == (expr, [])
    assert convert_array_to_matrix(expr) == _array_contraction(_array_tensor_product(A, B, C), (1, 2, 4))

    expr = _array_contraction(_array_tensor_product(A, I, I), (1, 2, 4))
    assert _array_contraction_to_diagonal_multiple_identity(expr) == (A, [2])
    assert convert_array_to_matrix(expr) == A

    expr = _array_contraction(_array_tensor_product(A, I, I, B), (1, 2, 4), (3, 6))
    assert _array_contraction_to_diagonal_multiple_identity(expr) == (expr, [])

    expr = _array_contraction(_array_tensor_product(A, I, I, B), (1, 2, 3, 4, 6))
    assert _array_contraction_to_diagonal_multiple_identity(expr) == (expr, [])

