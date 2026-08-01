
def test_undefind_kind():
    # Because of limitations in the kind dispatcher API, we are currently
    # unable to have OperatorKind*KetKind -> KetKind (and similar for bras).
    assert (A*k).kind == UndefinedKind
    assert (b*A).kind == UndefinedKind
    assert (x*b*A*k).kind == UndefinedKind

