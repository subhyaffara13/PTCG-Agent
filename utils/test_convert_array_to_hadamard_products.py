
def test_convert_array_to_hadamard_products():

    expr = HadamardProduct(M, N)
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == expr

    expr = HadamardProduct(M, N)*P
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == expr

    expr = Q*HadamardProduct(M, N)*P
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == expr

    expr = Q*HadamardProduct(M, N.T)*P
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == expr

    expr = HadamardProduct(M, N)*HadamardProduct(Q, P)
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert expr == ret

    expr = P.T*HadamardProduct(M, N)*HadamardProduct(Q, P)
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert expr == ret

    # ArrayDiagonal should be converted
    cg = _array_diagonal(_array_tensor_product(M, N, Q), (1, 3), (0, 2, 4))
    ret = convert_array_to_matrix(cg)
    expected = PermuteDims(_array_diagonal(_array_tensor_product(HadamardProduct(M.T, N.T), Q), (1, 2)), [1, 0, 2])
    assert expected == ret

    # Special case that should return the same expression:
    cg = _array_diagonal(_array_tensor_product(HadamardProduct(M, N), Q), (0, 2))
    ret = convert_array_to_matrix(cg)
    assert ret == cg

    # Hadamard products with traces:

    expr = Trace(HadamardProduct(M, N))
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == Trace(HadamardProduct(M.T, N.T))

    expr = Trace(A*HadamardProduct(M, N))
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == Trace(HadamardProduct(M, N)*A)

    expr = Trace(HadamardProduct(A, M)*N)
    cg = convert_matrix_to_array(expr)
    ret = convert_array_to_matrix(cg)
    assert ret == Trace(HadamardProduct(M.T, N)*A)

    # These should not be converted into Hadamard products:

    cg = _array_diagonal(_array_tensor_product(M, N), (0, 1, 2, 3))
    ret = convert_array_to_matrix(cg)
    assert ret == cg

    cg = _array_diagonal(_array_tensor_product(A), (0, 1))
    ret = convert_array_to_matrix(cg)
    assert ret == cg

    cg = _array_diagonal(_array_tensor_product(M, N, P), (0, 2, 4), (1, 3, 5))
    assert convert_array_to_matrix(cg) == HadamardProduct(M, N, P)

    cg = _array_diagonal(_array_tensor_product(M, N, P), (0, 3, 4), (1, 2, 5))
    assert convert_array_to_matrix(cg) == HadamardProduct(M, P, N.T)

    cg = _array_diagonal(_array_tensor_product(I, I1, x), (1, 4), (3, 5))
    assert convert_array_to_matrix(cg) == DiagMatrix(x)

