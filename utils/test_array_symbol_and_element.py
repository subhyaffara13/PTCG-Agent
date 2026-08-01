
def test_array_symbol_and_element():
    A = ArraySymbol("A", (2,))
    A0 = ArrayElement(A, (0,))
    A1 = ArrayElement(A, (1,))
    assert A[0] == A0
    assert A[1] != A0
    assert A.as_explicit() == ImmutableDenseNDimArray([A0, A1])

    A2 = tensorproduct(A, A)
    assert A2.shape == (2, 2)
    # TODO: not yet supported:
    # assert A2.as_explicit() == Array([[A[0]*A[0], A[1]*A[0]], [A[0]*A[1], A[1]*A[1]]])
    A3 = tensorcontraction(A2, (0, 1))
    assert A3.shape == ()
    # TODO: not yet supported:
    # assert A3.as_explicit() == Array([])

    A = ArraySymbol("A", (2, 3, 4))
    Ae = A.as_explicit()
    assert Ae == ImmutableDenseNDimArray(
        [[[ArrayElement(A, (i, j, k)) for k in range(4)] for j in range(3)] for i in range(2)])

    p = _permute_dims(A, Permutation(0, 2, 1))
    assert isinstance(p, PermuteDims)

    A = ArraySymbol("A", (2,))
    raises(IndexError, lambda: A[()])
    raises(IndexError, lambda: A[0, 1])
    raises(ValueError, lambda: A[-1])
    raises(ValueError, lambda: A[2])

    O = OneArray(3, 4)
    Z = ZeroArray(m, n)

    raises(IndexError, lambda: O[()])
    raises(IndexError, lambda: O[1, 2, 3])
    raises(ValueError, lambda: O[3, 0])
    raises(ValueError, lambda: O[0, 4])

    assert O[1, 2] == 1
    assert Z[1, 2] == 0

