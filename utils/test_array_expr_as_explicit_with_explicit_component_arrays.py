
def test_array_expr_as_explicit_with_explicit_component_arrays():
    # Test if .as_explicit() works with explicit-component arrays
    # nested in array expressions:
    from sympy.abc import x, y, z, t
    A = Array([[x, y], [z, t]])
    assert ArrayTensorProduct(A, A).as_explicit() == tensorproduct(A, A)
    assert ArrayDiagonal(A, (0, 1)).as_explicit() == tensordiagonal(A, (0, 1))
    assert ArrayContraction(A, (0, 1)).as_explicit() == tensorcontraction(A, (0, 1))
    assert ArrayAdd(A, A).as_explicit() == A + A
    assert ArrayElementwiseApplyFunc(sin, A).as_explicit() == A.applyfunc(sin)
    assert PermuteDims(A, [1, 0]).as_explicit() == permutedims(A, [1, 0])
    assert Reshape(A, [4]).as_explicit() == A.reshape(4)

