
def test_Symbol_kind():
    assert comm_x.kind is NumberKind
    assert noncomm_x.kind is UndefinedKind

