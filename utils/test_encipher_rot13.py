
def test_encipher_rot13():
    assert encipher_rot13("ABC") == "NOP"
    assert encipher_rot13("NOP") == "ABC"
    assert decipher_rot13("ABC") == "NOP"
    assert decipher_rot13("NOP") == "ABC"

