
def test_array_expr_construction_with_functions():

    tp = tensorproduct(M, N)
    assert tp == ArrayTensorProduct(M, N)

    expr = tensorproduct(A, eye(2))
    assert expr == ArrayTensorProduct(A, eye(2))

    # Contraction:

    expr = tensorcontraction(M, (0, 1))
    assert expr == ArrayContraction(M, (0, 1))

    expr = tensorcontraction(tp, (1, 2))
    assert expr == ArrayContraction(tp, (1, 2))

    expr = tensorcontraction(tensorcontraction(tp, (1, 2)), (0, 1))
    assert expr == ArrayContraction(tp, (0, 3), (1, 2))

    # Diagonalization:

    expr = tensordiagonal(M, (0, 1))
    assert expr == ArrayDiagonal(M, (0, 1))

    expr = tensordiagonal(tensordiagonal(tp, (0, 1)), (0, 1))
    assert expr == ArrayDiagonal(tp, (0, 1), (2, 3))

    # Permutation of dimensions:

    expr = permutedims(M, [1, 0])
    assert expr == PermuteDims(M, [1, 0])

    expr = permutedims(PermuteDims(tp, [1, 0, 2, 3]), [0, 1, 3, 2])
    assert expr == PermuteDims(tp, [1, 0, 3, 2])

    expr = PermuteDims(tp, index_order_new=["a", "b", "c", "d"], index_order_old=["d", "c", "b", "a"])
    assert expr == PermuteDims(tp, [3, 2, 1, 0])

    arr = Array(range(32)).reshape(2, 2, 2, 2, 2)
    expr = PermuteDims(arr, index_order_new=["a", "b", "c", "d", "e"], index_order_old=['b', 'e', 'a', 'd', 'c'])
    assert expr == PermuteDims(arr, [2, 0, 4, 3, 1])
    assert expr.as_explicit() == permutedims(arr, index_order_new=["a", "b", "c", "d", "e"], index_order_old=['b', 'e', 'a', 'd', 'c'])

