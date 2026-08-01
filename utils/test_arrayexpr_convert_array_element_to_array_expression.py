
def test_arrayexpr_convert_array_element_to_array_expression():
    A = ArraySymbol("A", (k,))
    B = ArraySymbol("B", (k,))

    s = Sum(A[i]*B[i], (i, 0, k-1))
    cg = convert_indexed_to_array(s)
    assert cg == ArrayContraction(ArrayTensorProduct(A, B), (0, 1))

    s = A[i]*B[i]
    cg = convert_indexed_to_array(s)
    assert cg == ArrayDiagonal(ArrayTensorProduct(A, B), (0, 1))

    s = A[i]*B[j]
    cg = convert_indexed_to_array(s, [i, j])
    assert cg == ArrayTensorProduct(A, B)
    cg = convert_indexed_to_array(s, [j, i])
    assert cg == ArrayTensorProduct(B, A)

    s = tanh(A[i]*B[j])
    cg = convert_indexed_to_array(s, [i, j])
    assert cg.dummy_eq(ArrayElementwiseApplyFunc(tanh, ArrayTensorProduct(A, B)))

