
def test_exception_matches():
    assert m.exception_matches()
    assert m.exception_matches_base()
    assert m.modulenotfound_exception_matches_base()

