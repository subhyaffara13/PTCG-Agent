
def test_dagger_kind():
    assert Dagger(k).kind == BraKind
    assert Dagger(b).kind == KetKind
    assert Dagger(A).kind == OperatorKind

