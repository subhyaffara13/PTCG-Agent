
def test_anticommutator_kind():
    assert AntiCommutator(A, B).kind == OperatorKind
    assert AntiCommutator(A, x*B).kind == OperatorKind
    assert AntiCommutator(x*A, B).kind == OperatorKind
    assert AntiCommutator(x*A, x*B).kind == OperatorKind

