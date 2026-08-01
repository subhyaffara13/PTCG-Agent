
def test_arrayexpr_convert_array_to_matrix2():
    cg = _array_contraction(_array_tensor_product(M, N), (1, 3))
    assert convert_array_to_matrix(cg) == M * N.T

    cg = PermuteDims(_array_tensor_product(M, N), Permutation([0, 1, 3, 2]))
    assert convert_array_to_matrix(cg) == _array_tensor_product(M, N.T)

    cg = _array_tensor_product(M, PermuteDims(N, Permutation([1, 0])))
    assert convert_array_to_matrix(cg) == _array_tensor_product(M, N.T)

    cg = _array_contraction(
        PermuteDims(
            _array_tensor_product(M, N, P, Q), Permutation([0, 2, 3, 1, 4, 5, 7, 6])),
        (1, 2), (3, 5)
    )
    assert convert_array_to_matrix(cg) == _array_tensor_product(M * P.T * Trace(N), Q.T)

    cg = _array_contraction(
        _array_tensor_product(M, N, P, PermuteDims(Q, Permutation([1, 0]))),
        (1, 5), (2, 3)
    )
    assert convert_array_to_matrix(cg) == _array_tensor_product(M * P.T * Trace(N), Q.T)

    cg = _array_tensor_product(M, PermuteDims(N, [1, 0]))
    assert convert_array_to_matrix(cg) == _array_tensor_product(M, N.T)

    cg = _array_tensor_product(PermuteDims(M, [1, 0]), PermuteDims(N, [1, 0]))
    assert convert_array_to_matrix(cg) == _array_tensor_product(M.T, N.T)

    cg = _array_tensor_product(PermuteDims(N, [1, 0]), PermuteDims(M, [1, 0]))
    assert convert_array_to_matrix(cg) == _array_tensor_product(N.T, M.T)

    cg = _array_contraction(M, (0,), (1,))
    assert convert_array_to_matrix(cg) == OneMatrix(1, k)*M*OneMatrix(k, 1)

    cg = _array_contraction(x, (0,), (1,))
    assert convert_array_to_matrix(cg) == OneMatrix(1, k)*x

    Xm = MatrixSymbol("Xm", m, n)
    cg = _array_contraction(Xm, (0,), (1,))
    assert convert_array_to_matrix(cg) == OneMatrix(1, m)*Xm*OneMatrix(n, 1)

