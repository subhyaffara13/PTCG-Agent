
def test_encipher_shift():
    assert encipher_shift("ABC", 0) == "ABC"
    assert encipher_shift("ABC", 1) == "BCD"
    assert encipher_shift("ABC", -1) == "ZAB"
    assert decipher_shift("ZAB", -1) == "ABC"

