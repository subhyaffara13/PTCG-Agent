
def test_encipher_atbash():
    assert encipher_atbash("ABC") == "ZYX"
    assert encipher_atbash("ZYX") == "ABC"
    assert decipher_atbash("ABC") == "ZYX"
    assert decipher_atbash("ZYX") == "ABC"

