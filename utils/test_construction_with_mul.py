
def test_construction_with_mul():
    assert mul(C, D) == MatMul(C, D)
    assert mul(D, C) == MatMul(D, C)
    assert mul(C, D) != MatMul(D, C)

