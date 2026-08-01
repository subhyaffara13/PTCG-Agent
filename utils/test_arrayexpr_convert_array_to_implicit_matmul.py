
def test_arrayexpr_convert_array_to_implicit_matmul():
    # Trivial dimensions are suppressed, so the result can be expressed in matrix form:

    cg = _array_tensor_product(a, b)
    assert convert_array_to_matrix(cg) == a * b.T

    cg = _array_tensor_product(a, b, I)
    assert convert_array_to_matrix(cg) == _array_tensor_product(a*b.T, I)

    cg = _array_tensor_product(I, a, b)
    assert convert_array_to_matrix(cg) == _array_tensor_product(I, a*b.T)

    cg = _array_tensor_product(a, I, b)
    assert convert_array_to_matrix(cg) == _array_tensor_product(a, I, b)

    cg = _array_contraction(_array_tensor_product(I, I), (1, 2))
    assert convert_array_to_matrix(cg) == I

    cg = PermuteDims(_array_tensor_product(I, Identity(1)), [0, 2, 1, 3])
    assert convert_array_to_matrix(cg) == I

