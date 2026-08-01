
def test_mul_kind():
    assert Mul(2,comm_x, evaluate=False).kind is NumberKind
    assert Mul(2,3, evaluate=False).kind is NumberKind
    assert Mul(noncomm_x,2, evaluate=False).kind is UndefinedKind
    assert Mul(2,noncomm_x, evaluate=False).kind is UndefinedKind

