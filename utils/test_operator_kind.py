
def test_operator_kind():
    assert A.kind == OperatorKind
    assert (A*B).kind == OperatorKind
    assert (x*A).kind == OperatorKind
    assert (x*A*B).kind == OperatorKind
    assert (x*k*b).kind == OperatorKind # outer product

