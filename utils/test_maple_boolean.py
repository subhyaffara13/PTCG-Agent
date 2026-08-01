
def test_maple_boolean():
    assert maple_code(True) == "true"
    assert maple_code(S.true) == "true"
    assert maple_code(False) == "false"
    assert maple_code(S.false) == "false"

