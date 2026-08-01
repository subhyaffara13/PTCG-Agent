
def test_construction_with_Mul():
    assert Mul(C, D) == MatMul(C, D)
    assert Mul(D, C) == MatMul(D, C)

