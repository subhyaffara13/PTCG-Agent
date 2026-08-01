
def test_array_as_explicit_matrix_symbol():

    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)

    texpr = tensorproduct(A, B)
    assert isinstance(texpr, ArrayTensorProduct)
    assert texpr.as_explicit() == tensorproduct(A.as_explicit(), B.as_explicit())

    texpr = tensorcontraction(A, (0, 1))
    assert isinstance(texpr, ArrayContraction)
    assert texpr.as_explicit() == A[0, 0] + A[1, 1] + A[2, 2]

    texpr = tensordiagonal(A, (0, 1))
    assert isinstance(texpr, ArrayDiagonal)
    assert texpr.as_explicit() == ImmutableDenseNDimArray([A[0, 0], A[1, 1], A[2, 2]])

    texpr = permutedims(A, [1, 0])
    assert isinstance(texpr, PermuteDims)
    assert texpr.as_explicit() == permutedims(A.as_explicit(), [1, 0])

    expr = ArrayAdd(ArrayTensorProduct(A, B), ArrayTensorProduct(B, A))
    assert expr.as_explicit() == expr.args[0].as_explicit() + expr.args[1].as_explicit()

