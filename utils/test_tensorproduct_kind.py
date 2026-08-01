
def test_tensorproduct_kind():
    assert TensorProduct(k,k).kind == KetKind
    assert TensorProduct(b,b).kind == BraKind
    assert TensorProduct(x*k,y*k).kind == KetKind
    assert TensorProduct(x*b,y*b).kind == BraKind
    assert TensorProduct(x*b*k, y*b*k).kind == NumberKind
    assert TensorProduct(x*k*b, y*k*b).kind == OperatorKind
    assert TensorProduct(A, B).kind == OperatorKind
    assert TensorProduct(A, x*B).kind == OperatorKind
    assert TensorProduct(x*A, B).kind == OperatorKind

