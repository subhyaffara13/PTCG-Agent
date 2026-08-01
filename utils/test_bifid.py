
def test_bifid():
    raises(ValueError, lambda: encipher_bifid('abc', 'b', 'abcde'))
    assert encipher_bifid('abc', 'b', 'abcd') == 'bdb'
    raises(ValueError, lambda: decipher_bifid('bdb', 'b', 'abcde'))
    assert encipher_bifid('bdb', 'b', 'abcd') == 'abc'
    raises(ValueError, lambda: bifid_square('abcde'))
    assert bifid5_square("B") == \
        bifid5_square('BACDEFGHIKLMNOPQRSTUVWXYZ')
    assert bifid6_square('B0') == \
        bifid6_square('B0ACDEFGHIJKLMNOPQRSTUVWXYZ123456789')

