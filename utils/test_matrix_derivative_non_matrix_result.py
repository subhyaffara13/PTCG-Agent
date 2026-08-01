
def test_matrix_derivative_non_matrix_result():
    # This is a 4-dimensional array:
    I = Identity(k)
    AdA = PermuteDims(ArrayTensorProduct(I, I), Permutation(3)(1, 2))
    assert A.diff(A) == AdA
    assert A.T.diff(A) == PermuteDims(ArrayTensorProduct(I, I), Permutation(3)(1, 2, 3))
    assert (2*A).diff(A) == PermuteDims(ArrayTensorProduct(2*I, I), Permutation(3)(1, 2))
    assert MatAdd(A, A).diff(A) == ArrayAdd(AdA, AdA)
    assert (A + B).diff(A) == AdA

