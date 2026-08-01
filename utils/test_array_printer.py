
def test_array_printer():
    A = ArraySymbol('A', (4,4,6,6,6))
    I = IndexedBase('I')
    i,j,k = Idx('i', (0,1)), Idx('j', (2,3)), Idx('k', (4,5))

    prntr = NumPyPrinter()
    assert prntr.doprint(ZeroArray(5)) == 'numpy.zeros((5,))'
    assert prntr.doprint(OneArray(5)) == 'numpy.ones((5,))'
    assert prntr.doprint(ArrayContraction(A, [2,3])) == 'numpy.einsum("abccd->abd", A)'
    assert prntr.doprint(I) == 'I'
    assert prntr.doprint(ArrayDiagonal(A, [2,3,4])) == 'numpy.einsum("abccc->abc", A)'
    assert prntr.doprint(ArrayDiagonal(A, [0,1], [2,3])) == 'numpy.einsum("aabbc->cab", A)'
    assert prntr.doprint(ArrayContraction(A, [2], [3])) == 'numpy.einsum("abcde->abe", A)'
    assert prntr.doprint(Assignment(I[i,j,k], I[i,j,k])) == 'I = I'

    prntr = TensorflowPrinter()
    assert prntr.doprint(ZeroArray(5)) == 'tensorflow.zeros((5,))'
    assert prntr.doprint(OneArray(5)) == 'tensorflow.ones((5,))'
    assert prntr.doprint(ArrayContraction(A, [2,3])) == 'tensorflow.linalg.einsum("abccd->abd", A)'
    assert prntr.doprint(I) == 'I'
    assert prntr.doprint(ArrayDiagonal(A, [2,3,4])) == 'tensorflow.linalg.einsum("abccc->abc", A)'
    assert prntr.doprint(ArrayDiagonal(A, [0,1], [2,3])) == 'tensorflow.linalg.einsum("aabbc->cab", A)'
    assert prntr.doprint(ArrayContraction(A, [2], [3])) == 'tensorflow.linalg.einsum("abcde->abe", A)'
    assert prntr.doprint(Assignment(I[i,j,k], I[i,j,k])) == 'I = I'

