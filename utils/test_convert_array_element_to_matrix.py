
def test_convert_array_element_to_matrix():

    expr = ArrayElement(M, (i, j))
    assert convert_array_to_matrix(expr) == MatrixElement(M, i, j)

    expr = ArrayElement(_array_contraction(_array_tensor_product(M, N), (1, 3)), (i, j))
    assert convert_array_to_matrix(expr) == MatrixElement(M*N.T, i, j)

    expr = ArrayElement(_array_tensor_product(M, N), (i, j, m, n))
    assert convert_array_to_matrix(expr) == expr

