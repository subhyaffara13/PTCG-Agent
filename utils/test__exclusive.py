
def test_Exclusive():
    assert Exclusive(False, False, False) is true
    assert Exclusive(True, False, False) is true
    assert Exclusive(True, True, False) is false
    assert Exclusive(True, True, True) is false

