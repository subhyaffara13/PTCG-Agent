
def test_encipher_substitution():
    assert encipher_substitution("ABC", "BAC", "ABC") == "BAC"
    assert encipher_substitution("123", "1243", "1234") == "124"

