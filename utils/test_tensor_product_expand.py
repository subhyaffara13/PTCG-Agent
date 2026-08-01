
def test_tensor_product_expand():
    assert TP(A + B, B + C).expand(tensorproduct=True) == \
        TP(A, B) + TP(A, C) + TP(B, B) + TP(B, C)
    #Tests for fix of issue #24142
    assert TP(A-B, B-A).expand(tensorproduct=True) == \
        TP(A, B) - TP(A, A) - TP(B, B) + TP(B, A)
    assert TP(2*A + B, A + B).expand(tensorproduct=True) == \
        2 * TP(A, A) + 2 * TP(A, B) + TP(B, A) + TP(B, B)
    assert TP(2 * A * B + A, A + B).expand(tensorproduct=True) == \
        2 * TP(A*B, A) + 2 * TP(A*B, B) + TP(A, A) + TP(A, B)

