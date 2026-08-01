
def test_arrayexpr_convert_indexed_to_array_expression():

    s = Sum(A[i]*B[i], (i, 0, 3))
    cg = convert_indexed_to_array(s)
    assert cg == ArrayContraction(ArrayTensorProduct(A, B), (0, 1))

    expr = M*N
    result = ArrayContraction(ArrayTensorProduct(M, N), (1, 2))
    elem = expr[i, j]
    assert convert_indexed_to_array(elem) == result

    expr = M*N*M
    elem = expr[i, j]
    result = _array_contraction(_array_tensor_product(M, M, N), (1, 4), (2, 5))
    cg = convert_indexed_to_array(elem)
    assert cg == result

    cg = convert_indexed_to_array((M * N * P)[i, j])
    assert cg == _array_contraction(ArrayTensorProduct(M, N, P), (1, 2), (3, 4))

    cg = convert_indexed_to_array((M * N.T * P)[i, j])
    assert cg == _array_contraction(ArrayTensorProduct(M, N, P), (1, 3), (2, 4))

    expr = -2*M*N
    elem = expr[i, j]
    cg = convert_indexed_to_array(elem)
    assert cg == ArrayContraction(ArrayTensorProduct(-2, M, N), (1, 2))

