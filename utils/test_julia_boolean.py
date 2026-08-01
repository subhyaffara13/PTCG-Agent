
def test_julia_boolean():
    assert julia_code(True) == "true"
    assert julia_code(S.true) == "true"
    assert julia_code(False) == "false"
    assert julia_code(S.false) == "false"

