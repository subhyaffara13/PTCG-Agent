
def test_combine_powers():
    assert combine_powers(MatMul(D, Inverse(D), D, evaluate=False)) == \
                 MatMul(Identity(n), D, evaluate=False)
    assert combine_powers(MatMul(B.T, Inverse(E*A), E, A, B, evaluate=False)) == \
        MatMul(B.T, Identity(m), B, evaluate=False)
    assert combine_powers(MatMul(A, E, Inverse(A*E), D, evaluate=False)) == \
        MatMul(Identity(n), D, evaluate=False)


def test_combine_powers():
    assert (C ** 1) ** 1 == C
    assert (C ** 2) ** 3 == MatPow(C, 6)
    assert (C ** -2) ** -3 == MatPow(C, 6)
    assert (C ** -1) ** -1 == C
    assert (((C ** 2) ** 3) ** 4) ** 5 == MatPow(C, 120)
    assert (C ** n) ** n == C ** (n ** 2)

