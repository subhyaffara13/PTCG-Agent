
def test_commutator_kind():
    assert Commutator(A, B).kind == OperatorKind
    assert Commutator(A, x*B).kind == OperatorKind
    assert Commutator(x*A, B).kind == OperatorKind
    assert Commutator(x*A, x*B).kind == OperatorKind

