
def test_encipher_affine():
    assert encipher_affine("ABC", (1, 0)) == "ABC"
    assert encipher_affine("ABC", (1, 1)) == "BCD"
    assert encipher_affine("ABC", (-1, 0)) == "AZY"
    assert encipher_affine("ABC", (-1, 1), symbols="ABCD") == "BAD"
    assert encipher_affine("123", (-1, 1), symbols="1234") == "214"
    assert encipher_affine("ABC", (3, 16)) == "QTW"
    assert decipher_affine("QTW", (3, 16)) == "ABC"

