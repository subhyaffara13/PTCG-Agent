
def test_Add_kind():
    assert Add(2, 3, evaluate=False).kind is NumberKind
    assert Add(2,comm_x).kind is NumberKind
    assert Add(2,noncomm_x).kind is UndefinedKind

