
def test_array_element_expressions():
    # Check commutative property:
    assert M[0, 0]*N[0, 0] == N[0, 0]*M[0, 0]

    # Check derivatives:
    assert M[0, 0].diff(M[0, 0]) == 1
    assert M[0, 0].diff(M[1, 0]) == 0
    assert M[0, 0].diff(N[0, 0]) == 0
    assert M[0, 1].diff(M[i, j]) == KroneckerDelta(i, 0)*KroneckerDelta(j, 1)
    assert M[0, 1].diff(N[i, j]) == 0

    K4 = ArraySymbol("K4", shape=(k, k, k, k))

    assert K4[i, j, k, l].diff(K4[1, 2, 3, 4]) == (
        KroneckerDelta(i, 1)*KroneckerDelta(j, 2)*KroneckerDelta(k, 3)*KroneckerDelta(l, 4)
    )

