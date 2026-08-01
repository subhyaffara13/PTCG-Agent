
def test_issue_10633():
    assert Eq(True, False) == False
    assert Eq(False, True) == False
    assert Eq(True, True) == True
    assert Eq(False, False) == True

