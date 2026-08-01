
def test_type_mro():
    assert super_signature([[object], [type]]) == [type]

