
def test_accept_int():
    assert not Float(4) == 4
    assert Float(4) != 4
    assert Float(4) == 4.0

