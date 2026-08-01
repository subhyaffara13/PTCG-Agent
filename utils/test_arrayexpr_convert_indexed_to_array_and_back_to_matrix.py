
def test_arrayexpr_convert_indexed_to_array_and_back_to_matrix():

    expr = a.T*b
    elem = expr[0, 0]
    cg = convert_indexed_to_array(elem)
    assert cg == ArrayElement(ArrayContraction(ArrayTensorProduct(a, b), (0, 2)), [0, 0])

    expr = M[i,j] + N[i,j]
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == M + N

    expr = M[i,j] + N[j,i]
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == M + N.T

    expr = M[i,j]*N[k,l] + N[i,j]*M[k,l]
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == ArrayAdd(
        ArrayTensorProduct(M, N),
        ArrayTensorProduct(N, M))

    expr = (M*N*P)[i, j]
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == M * N * P

    expr = Sum(M[i,j]*(N*P)[j,m], (j, 0, k-1))
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == M * N * P

    expr = Sum((P[j, m] + P[m, j])*(M[i,j]*N[m,n] + N[i,j]*M[m,n]), (j, 0, k-1), (m, 0, k-1))
    p1, p2 = _convert_indexed_to_array(expr)
    assert convert_array_to_matrix(p1) == M * P * N + M * P.T * N + N * P * M + N * P.T * M

