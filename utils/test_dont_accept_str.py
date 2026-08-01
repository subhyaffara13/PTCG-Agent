
def test_dont_accept_str():
    assert Float("0.2") != "0.2"
    assert not (Float("0.2") == "0.2")

