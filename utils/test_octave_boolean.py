
def test_octave_boolean():
    assert mcode(True) == "true"
    assert mcode(S.true) == "true"
    assert mcode(False) == "false"
    assert mcode(S.false) == "false"

